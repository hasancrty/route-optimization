"""
genetic_algorithm.py
---------------------
TSP için Genetik Algoritma.

Bileşenler:
    - Popülasyon: rastgele turlardan oluşan başlangıç kümesi
    - Seçilim: turnuva seçimi (tournament selection)
    - Çaprazlama: sıralı çaprazlama (Order Crossover / OX) — TSP için geçerli
      permütasyonlar üretir
    - Mutasyon: iki şehrin yerini değiştirme (swap mutation)
    - Elitizm: en iyi bireyler doğrudan bir sonraki nesle aktarılır
"""

from __future__ import annotations

import random
from typing import List, Sequence, Tuple

from ..distance import tour_length


def _tournament_selection(population: List[List[int]], fitnesses: List[float], k: int, rng: random.Random) -> List[int]:
    contenders = rng.sample(range(len(population)), k)
    best_idx = min(contenders, key=lambda i: fitnesses[i])
    return population[best_idx]


def _order_crossover(parent1: List[int], parent2: List[int], rng: random.Random) -> List[int]:
    n = len(parent1)
    a, b = sorted(rng.sample(range(n), 2))
    child: List[int | None] = [None] * n
    child[a:b] = parent1[a:b]
    fill_values = [g for g in parent2 if g not in child[a:b]]
    idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill_values[idx]
            idx += 1
    return child  # type: ignore[return-value]


def _swap_mutation(tour: List[int], mutation_rate: float, rng: random.Random) -> List[int]:
    tour = tour[:]
    for i in range(len(tour)):
        if rng.random() < mutation_rate:
            j = rng.randrange(len(tour))
            tour[i], tour[j] = tour[j], tour[i]
    return tour


def genetic_algorithm(
    dist_matrix: Sequence[Sequence[float]],
    population_size: int = 100,
    generations: int = 300,
    mutation_rate: float = 0.02,
    tournament_k: int = 5,
    elitism_count: int = 4,
    seed: int | None = None,
) -> Tuple[List[int], List[float]]:
    """
    Returns:
        best_tour: bulunan en iyi tur
        history: nesil başına en iyi mesafe (yakınsama grafiği için)
    """
    rng = random.Random(seed)
    n = len(dist_matrix)
    base = list(range(n))

    population = [rng.sample(base, n) for _ in range(population_size)]
    history: List[float] = []

    best_tour = population[0]
    best_len = tour_length(best_tour, dist_matrix)

    for _ in range(generations):
        fitnesses = [tour_length(ind, dist_matrix) for ind in population]

        gen_best_idx = min(range(population_size), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] < best_len:
            best_len = fitnesses[gen_best_idx]
            best_tour = population[gen_best_idx][:]
        history.append(best_len)

        ranked = sorted(range(population_size), key=lambda i: fitnesses[i])
        new_population = [population[i][:] for i in ranked[:elitism_count]]  # elitizm

        while len(new_population) < population_size:
            p1 = _tournament_selection(population, fitnesses, tournament_k, rng)
            p2 = _tournament_selection(population, fitnesses, tournament_k, rng)
            child = _order_crossover(p1, p2, rng)
            child = _swap_mutation(child, mutation_rate, rng)
            new_population.append(child)

        population = new_population

    return best_tour, history
