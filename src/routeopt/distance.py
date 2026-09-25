"""
distance.py
-----------
Noktalar arası mesafe hesaplama fonksiyonları ve mesafe matrisi üretimi.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

EARTH_RADIUS_KM = 6371.0088


def euclidean(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Düzlemsel (kartezyen) mesafe."""
    return math.dist(p1, p2)


def haversine(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    İki (enlem, boylam) noktası arasındaki büyük çember (haversine) mesafesini
    kilometre cinsinden döndürür. Gerçek coğrafi koordinatlarla çalışırken kullanılır.
    """
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return EARTH_RADIUS_KM * c


def build_distance_matrix(
    points: Sequence[Tuple[float, float]], metric: str = "euclidean"
) -> List[List[float]]:
    """
    Noktalar listesinden NxN mesafe matrisi üretir.

    Args:
        points: [(x, y), ...] veya [(lat, lon), ...]
        metric: "euclidean" veya "haversine"
    """
    fn = haversine if metric == "haversine" else euclidean
    n = len(points)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = fn(points[i], points[j])
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix


def tour_length(tour: Sequence[int], dist_matrix: Sequence[Sequence[float]], cyclic: bool = True) -> float:
    """Bir turun (indeks dizisi) toplam uzunluğunu hesaplar."""
    total = 0.0
    n = len(tour)
    for i in range(n - 1):
        total += dist_matrix[tour[i]][tour[i + 1]]
    if cyclic and n > 1:
        total += dist_matrix[tour[-1]][tour[0]]
    return total
