"""
vrp.py
------
Kapasiteli Araç Rotalama Problemi (Capacitated Vehicle Routing Problem - CVRP).

Tek bir deponun (depot) birden fazla aracı olduğu, her müşterinin bir talebi
(demand) bulunduğu ve her aracın kapasitesi sınırlı olduğu senaryoyu çözer.

Kullanılan yöntem: Clarke & Wright Tasarruf (Savings) Algoritması
    1. Her müşteri için depo-müşteri-depo şeklinde ayrı bir rota ile başla.
    2. İki rotayı birleştirmenin sağladığı "tasarrufu" hesapla:
           saving(i, j) = d(depot, i) + d(depot, j) - d(i, j)
    3. Tasarrufları büyükten küçüğe sırala, kapasiteyi aşmayan ve geçerli
       (uç noktalardan) birleşimleri sırayla uygula.

Bu, endüstride yaygın kullanılan, hızlı ve anlaşılır bir klasik sezgiseldir.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple

from .distance import tour_length


@dataclass
class VRPResult:
    routes: List[List[int]]  # her rota: depo hariç müşteri indeksleri
    route_loads: List[float]
    route_distances: List[float]
    total_distance: float
    vehicles_used: int


def clarke_wright_savings(
    dist_matrix: Sequence[Sequence[float]],
    demands: Sequence[float],
    vehicle_capacity: float,
    depot: int = 0,
) -> VRPResult:
    customers = [i for i in range(len(dist_matrix)) if i != depot]

    # Başlangıç: her müşteri kendi rotasında (depo - müşteri - depo)
    routes: Dict[int, List[int]] = {c: [c] for c in customers}
    route_of: Dict[int, int] = {c: c for c in customers}  # müşteri -> rota anahtarı

    # Tasarrufları hesapla
    savings: List[Tuple[float, int, int]] = []
    for i in customers:
        for j in customers:
            if i < j:
                s = (
                    dist_matrix[depot][i]
                    + dist_matrix[depot][j]
                    - dist_matrix[i][j]
                )
                savings.append((s, i, j))
    savings.sort(key=lambda x: x[0], reverse=True)

    def route_load(route: List[int]) -> float:
        return sum(demands[c] for c in route)

    for s, i, j in savings:
        if s <= 0:
            continue
        ri, rj = route_of[i], route_of[j]
        if ri == rj:
            continue  # zaten aynı rotada

        route_i, route_j = routes[ri], routes[rj]

        # Birleştirme yalnızca i ve j birer rotanın UÇ noktasıysa (Clarke-Wright kuralı) geçerlidir.
        i_is_end = route_i[0] == i or route_i[-1] == i
        j_is_end = route_j[0] == j or route_j[-1] == j
        if not (i_is_end and j_is_end):
            continue

        if route_load(route_i) + route_load(route_j) > vehicle_capacity:
            continue

        # i sonda, j başta olacak şekilde yönlendir
        if route_i[-1] != i:
            route_i = route_i[::-1]
        if route_j[0] != j:
            route_j = route_j[::-1]

        merged = route_i + route_j
        new_key = ri
        routes[new_key] = merged
        del routes[rj]
        for c in merged:
            route_of[c] = new_key

    final_routes = list(routes.values())
    route_loads = [route_load(r) for r in final_routes]
    route_distances = [
        dist_matrix[depot][r[0]]
        + sum(dist_matrix[r[k]][r[k + 1]] for k in range(len(r) - 1))
        + dist_matrix[r[-1]][depot]
        for r in final_routes
    ]

    return VRPResult(
        routes=final_routes,
        route_loads=route_loads,
        route_distances=route_distances,
        total_distance=sum(route_distances),
        vehicles_used=len(final_routes),
    )
