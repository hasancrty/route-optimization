"""
nearest_neighbor.py
--------------------
Açgözlü (greedy) En Yakın Komşu sezgiseli.

Basit, hızlı (O(n^2)) ama optimalden genelde %20-30 uzak sonuçlar üretir.
Diğer algoritmalar (2-opt, SA, GA) için iyi bir başlangıç turu sağlar.
"""

from __future__ import annotations

from typing import List, Sequence


def nearest_neighbor_tour(dist_matrix: Sequence[Sequence[float]], start: int = 0) -> List[int]:
    n = len(dist_matrix)
    if n == 0:
        return []
    unvisited = set(range(n))
    unvisited.discard(start)
    tour = [start]
    current = start

    while unvisited:
        next_city = min(unvisited, key=lambda c: dist_matrix[current][c])
        tour.append(next_city)
        unvisited.discard(next_city)
        current = next_city

    return tour
