"""
example_vrp.py
---------------
Kapasiteli Araç Rotalama Problemi (CVRP) örneği.

Çalıştırma:
    python examples/example_vrp.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from routeopt.data_generator import generate_vrp_instance
from routeopt.distance import build_distance_matrix
from routeopt.visualize import plot_vrp_routes
from routeopt.vrp import clarke_wright_savings


def main():
    points, demands = generate_vrp_instance(n_customers=24, min_demand=5, max_demand=20, seed=7)
    dist_matrix = build_distance_matrix(points)

    result = clarke_wright_savings(dist_matrix, demands, vehicle_capacity=60)

    print(f"Kullanılan araç sayısı: {result.vehicles_used}")
    print(f"Toplam mesafe: {result.total_distance:.2f}\n")
    for i, (route, load, dist) in enumerate(zip(result.routes, result.route_loads, result.route_distances)):
        print(f"Araç {i + 1}: {route}")
        print(f"   Yük: {load:.0f} / 60   Mesafe: {dist:.2f}")

    plot_vrp_routes(points, result.routes, save_path="example_vrp.png")
    print("\nGörsel kaydedildi: example_vrp.png")


if __name__ == "__main__":
    main()
