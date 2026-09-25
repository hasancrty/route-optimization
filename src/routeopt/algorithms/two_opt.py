"""
two_opt.py
----------
2-opt lokal arama iyileştirmesi.

Bir tur içindeki iki kenarı seçip aralarındaki segmenti ters çevirerek
(çapraz kesişen yolları açarak) toplam mesafeyi azaltmaya çalışır.
Nearest Neighbor gibi bir başlangıç turunu iyileştirmek için kullanılır.
"""

from __future__ import annotations

from typing import List, Sequence

from ..distance import tour_length


def two_opt(
    tour: List[int],
    dist_matrix: Sequence[Sequence[float]],
    max_iterations: int = 1000,
) -> List[int]:
    best = tour[:]
    best_len = tour_length(best, dist_matrix)
    improved = True
    iterations = 0

    n = len(best)
    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if j - i == 1:
                    continue  # komşu kenarlar, anlamsız swap
                new_tour = best[:i] + best[i:j][::-1] + best[j:]
                new_len = tour_length(new_tour, dist_matrix)
                if new_len < best_len - 1e-9:
                    best = new_tour
                    best_len = new_len
                    improved = True
        # improved True kaldıkça tekrar tara (first-improvement + tekrar tarama)

    return best
