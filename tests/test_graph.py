import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from routeopt.graph import Graph, astar, dijkstra, reconstruct_path


def build_sample_graph() -> Graph:
    g = Graph()
    g.add_node("A", (0, 0))
    g.add_node("B", (1, 0))
    g.add_node("C", (1, 1))
    g.add_node("D", (2, 1))
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 1)
    g.add_edge("C", "D", 1)
    g.add_edge("A", "D", 5)
    return g


def test_dijkstra_finds_shortest_path():
    g = build_sample_graph()
    dist, prev = dijkstra(g, "A")
    assert dist["D"] == 3  # A->B->C->D (1+1+1) < A->D (5)
    path = reconstruct_path(prev, "A", "D")
    assert path == ["A", "B", "C", "D"]


def test_dijkstra_unreachable_node():
    g = Graph()
    g.add_node("X")
    g.add_node("Y")  # bağlantısız
    dist, _ = dijkstra(g, "X")
    import math

    assert dist["Y"] == math.inf


def test_astar_matches_dijkstra_result():
    g = build_sample_graph()
    dist, _ = dijkstra(g, "A", "D")
    total, path = astar(g, "A", "D")
    assert total == dist["D"]
    assert path[0] == "A" and path[-1] == "D"


def test_graph_add_edge_undirected_symmetry():
    g = Graph()
    g.add_edge("A", "B", 5)
    assert g.neighbors("A")["B"] == 5
    assert g.neighbors("B")["A"] == 5
