"""
example_basic.py
-----------------
Farklı TSP algoritmalarının aynı veri üzerinde nasıl kullanılacağını gösteren
basit bir örnek.

Çalıştırma:
    python examples/example_basic.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from routeopt.algorithms import genetic_algorithm, nearest_neighbor_tour, simulated_annealing, two_opt
from routeopt.data_generator import generate_random_points
from routeopt.distance import build_distance_matrix, tour_length
from routeopt.visualize import plot_convergence, plot_tour


def main():
    points = generate_random_points(30, seed=42)
    dist_matrix = build_distance_matrix(points)

    # 1) Nearest Neighbor (hızlı başlangıç turu)
    nn_tour = nearest_neighbor_tour(dist_matrix)
    print(f"Nearest Neighbor: {tour_length(nn_tour, dist_matrix):.2f}")

    # 2) 2-opt ile iyileştirme
    improved_tour = two_opt(nn_tour, dist_matrix)
    print(f"2-opt sonrası:    {tour_length(improved_tour, dist_matrix):.2f}")

    # 3) Simulated Annealing
    sa_tour, sa_history = simulated_annealing(dist_matrix, nn_tour, seed=42)
    print(f"Simulated Ann.:   {tour_length(sa_tour, dist_matrix):.2f}")

    # 4) Genetic Algorithm
    ga_tour, ga_history = genetic_algorithm(dist_matrix, generations=300, seed=42)
    print(f"Genetic Algo:     {tour_length(ga_tour, dist_matrix):.2f}")

    # Görselleri kaydet
    plot_tour(points, improved_tour, title="2-opt Rotası", save_path="example_2opt.png")
    plot_convergence(ga_history, title="GA Yakınsaması", save_path="example_ga_convergence.png")
    print("\nGörseller kaydedildi: example_2opt.png, example_ga_convergence.png")


if __name__ == "__main__":
    main()
