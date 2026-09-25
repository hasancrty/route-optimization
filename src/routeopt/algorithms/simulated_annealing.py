"""
simulated_annealing.py
-----------------------
Tavlama Benzetimi (Simulated Annealing) ile TSP çözümü.

Yerel optimumlara takılmamak için, başlangıçta kötü çözümleri de belirli bir
olasılıkla kabul eder; bu olasılık zamanla (sıcaklık düştükçe) azalır.
"""

from __future__ import annotations

import math
import random
from typing import List, Sequence, Tuple

from ..distance import tour_length


def simulated_annealing(
    dist_matrix: Sequence[Sequence[float]],
    initial_tour: List[int],
    initial_temp: float = 10_000.0,
    cooling_rate: float = 0.995,
    min_temp: float = 1e-3,
    iterations_per_temp: int = 100,
    seed: int | None = None,
) -> Tuple[List[int], List[float]]:
    """
    Returns:
        best_tour: bulunan en iyi tur
        history: her sıcaklık adımındaki en iyi mesafenin geçmişi (yakınsama grafiği için)
    """
    rng = random.Random(seed)
    n = len(initial_tour)

    current = initial_tour[:]
    current_len = tour_length(current, dist_matrix)
    best = current[:]
    best_len = current_len

    temp = initial_temp
    history: List[float] = [best_len]

    while temp > min_temp:
        for _ in range(iterations_per_temp):
            i, j = sorted(rng.sample(range(n), 2))
            if j - i < 1:
                continue
            candidate = current[:i] + current[i : j + 1][::-1] + current[j + 1 :]
            candidate_len = tour_length(candidate, dist_matrix)
            delta = candidate_len - current_len

            if delta < 0 or rng.random() < math.exp(-delta / temp):
                current, current_len = candidate, candidate_len
                if current_len < best_len:
                    best, best_len = current[:], current_len

        history.append(best_len)
        temp *= cooling_rate

    return best, history
