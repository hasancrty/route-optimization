"""
graph.py
--------
Ağırlıklı graf üzerinde en kısa yol hesaplamaları.

İçerik:
    - Graph: komşuluk listesi tabanlı, yönsüz/yönlü ağırlıklı graf
    - dijkstra(): klasik en kısa yol algoritması
    - astar(): sezgisel (heuristic) destekli en kısa yol algoritması

Bu modül; şehir/nokta ağları (yol ağı, teslimat noktaları vb.) üzerinde
iki nokta arasındaki en kısa/en ucuz yolu bulmak için kullanılır.
"""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field
from typing import Callable, Dict, Hashable, List, Optional, Tuple


Node = Hashable


@dataclass
class Graph:
    """Ağırlıklı graf. Düğümler herhangi bir hashable nesne olabilir (str, int, tuple...)."""

    directed: bool = False
    _adj: Dict[Node, Dict[Node, float]] = field(default_factory=dict)
    _coords: Dict[Node, Tuple[float, float]] = field(default_factory=dict)

    def add_node(self, node: Node, coord: Optional[Tuple[float, float]] = None) -> None:
        self._adj.setdefault(node, {})
        if coord is not None:
            self._coords[node] = coord

    def add_edge(self, u: Node, v: Node, weight: float) -> None:
        if weight < 0:
            raise ValueError("Negatif ağırlıklı kenarlara izin verilmiyor (Dijkstra için).")
        self.add_node(u)
        self.add_node(v)
        self._adj[u][v] = weight
        if not self.directed:
            self._adj[v][u] = weight

    def neighbors(self, node: Node) -> Dict[Node, float]:
        return self._adj.get(node, {})

    def nodes(self) -> List[Node]:
        return list(self._adj.keys())

    def coord(self, node: Node) -> Optional[Tuple[float, float]]:
        return self._coords.get(node)

    def __len__(self) -> int:
        return len(self._adj)

    def __contains__(self, node: Node) -> bool:
        return node in self._adj


def dijkstra(
    graph: Graph, source: Node, target: Optional[Node] = None
) -> Tuple[Dict[Node, float], Dict[Node, Optional[Node]]]:
    """
    Dijkstra algoritması ile `source` düğümünden diğer tüm düğümlere (veya
    verilirse yalnızca `target`'a) en kısa mesafeleri hesaplar.

    Returns:
        dist: her düğüm için en kısa mesafe sözlüğü
        prev: en kısa yol ağacı (geri iz sürmek için önceki düğüm)
    """
    if source not in graph:
        raise KeyError(f"'{source}' graf içinde bulunamadı.")

    dist: Dict[Node, float] = {n: math.inf for n in graph.nodes()}
    prev: Dict[Node, Optional[Node]] = {n: None for n in graph.nodes()}
    dist[source] = 0.0

    visited = set()
    pq: List[Tuple[float, Node]] = [(0.0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        if target is not None and u == target:
            break

        for v, w in graph.neighbors(u).items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev


def reconstruct_path(prev: Dict[Node, Optional[Node]], source: Node, target: Node) -> List[Node]:
    """prev haritasından source->target yolunu geri kurar."""
    if target not in prev:
        return []
    path: List[Node] = []
    cur: Optional[Node] = target
    while cur is not None:
        path.append(cur)
        if cur == source:
            break
        cur = prev.get(cur)
    path.reverse()
    if not path or path[0] != source:
        return []  # yol yok
    return path


def euclidean_heuristic(graph: Graph) -> Callable[[Node, Node], float]:
    """A* için düğüm koordinatlarına dayalı öklid mesafesi sezgiseli üretir."""

    def h(a: Node, b: Node) -> float:
        ca, cb = graph.coord(a), graph.coord(b)
        if ca is None or cb is None:
            return 0.0  # koordinat yoksa Dijkstra'ya düşer (kabul edilebilir/tutarlı h=0)
        return math.dist(ca, cb)

    return h


def astar(
    graph: Graph,
    source: Node,
    target: Node,
    heuristic: Optional[Callable[[Node, Node], float]] = None,
) -> Tuple[float, List[Node]]:
    """
    A* algoritması. `heuristic` verilmezse graf koordinatlarından öklid
    sezgiseli otomatik üretilir (koordinat yoksa Dijkstra'ya eşdeğer davranır).

    Returns:
        (toplam_mesafe, yol_listesi)
    """
    if source not in graph or target not in graph:
        raise KeyError("source/target graf içinde bulunamadı.")

    h = heuristic or euclidean_heuristic(graph)

    g_score: Dict[Node, float] = {n: math.inf for n in graph.nodes()}
    g_score[source] = 0.0
    prev: Dict[Node, Optional[Node]] = {n: None for n in graph.nodes()}

    open_set: List[Tuple[float, Node]] = [(h(source, target), source)]
    visited = set()

    while open_set:
        _, u = heapq.heappop(open_set)
        if u == target:
            break
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph.neighbors(u).items():
            tentative = g_score[u] + w
            if tentative < g_score[v]:
                g_score[v] = tentative
                prev[v] = u
                f = tentative + h(v, target)
                heapq.heappush(open_set, (f, v))

    path = reconstruct_path(prev, source, target)
    total = g_score.get(target, math.inf)
    return total, path
