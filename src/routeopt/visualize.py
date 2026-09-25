"""
visualize.py
------------
Rotaları ve algoritma yakınsama grafiklerini matplotlib ile çizip
PNG dosyası olarak kaydeden yardımcı fonksiyonlar.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")  # sunucu/CLI ortamında ekran olmadan çalışabilmek için
import matplotlib.pyplot as plt


def plot_tour(
    points: Sequence[Tuple[float, float]],
    tour: Sequence[int],
    title: str = "Rota",
    save_path: str = "tour.png",
) -> None:
    xs = [points[i][0] for i in tour] + [points[tour[0]][0]]
    ys = [points[i][1] for i in tour] + [points[tour[0]][1]]

    plt.figure(figsize=(8, 6))
    plt.plot(xs, ys, "o-", color="#2563eb", markersize=6, linewidth=1.5)
    plt.scatter(xs[0], ys[0], color="#dc2626", s=120, zorder=5, label="Başlangıç")
    for idx, i in enumerate(tour):
        plt.annotate(str(i), (points[i][0], points[i][1]), fontsize=8, xytext=(3, 3), textcoords="offset points")
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_convergence(history: Sequence[float], title: str = "Yakınsama Grafiği", save_path: str = "convergence.png") -> None:
    plt.figure(figsize=(8, 5))
    plt.plot(history, color="#16a34a", linewidth=2)
    plt.title(title)
    plt.xlabel("İterasyon / Nesil")
    plt.ylabel("En İyi Mesafe")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_vrp_routes(
    points: Sequence[Tuple[float, float]],
    routes: List[List[int]],
    depot: int = 0,
    title: str = "Araç Rotaları (VRP)",
    save_path: str = "vrp_routes.png",
) -> None:
    colors = plt.cm.tab10.colors
    plt.figure(figsize=(9, 7))

    for idx, route in enumerate(routes):
        full = [depot] + route + [depot]
        xs = [points[i][0] for i in full]
        ys = [points[i][1] for i in full]
        color = colors[idx % len(colors)]
        plt.plot(xs, ys, "o-", color=color, linewidth=1.5, markersize=5, label=f"Araç {idx + 1}")

    dx, dy = points[depot]
    plt.scatter([dx], [dy], color="black", marker="s", s=150, zorder=5, label="Depo")

    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(loc="best", fontsize=8)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_algorithm_comparison(results: Dict[str, float], save_path: str = "comparison.png") -> None:
    """Farklı algoritmaların bulduğu tur uzunluklarını çubuk grafikle karşılaştırır."""
    names = list(results.keys())
    values = list(results.values())

    plt.figure(figsize=(8, 5))
    bars = plt.bar(names, values, color="#7c3aed")
    for bar, v in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, v, f"{v:.1f}", ha="center", va="bottom", fontsize=9)
    plt.title("Algoritma Karşılaştırması (Tur Uzunluğu)")
    plt.ylabel("Toplam Mesafe")
    plt.xticks(rotation=20)
    plt.grid(alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
