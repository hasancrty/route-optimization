"""
cli.py
------
RouteOpt için komut satırı arayüzü.

Kullanım örnekleri:
    python -m routeopt.cli tsp --n 30 --algo two_opt --seed 42
    python -m routeopt.cli tsp --n 40 --algo ga --generations 500
    python -m routeopt.cli vrp --n 25 --capacity 50 --seed 7
    python -m routeopt.cli compare --n 30 --seed 1
"""

from __future__ import annotations

import argparse
import time

from .algorithms import genetic_algorithm, nearest_neighbor_tour, simulated_annealing, two_opt
from .data_generator import generate_random_points, generate_vrp_instance
from .distance import build_distance_matrix, tour_length
from .visualize import plot_algorithm_comparison, plot_convergence, plot_tour, plot_vrp_routes
from .vrp import clarke_wright_savings


def cmd_tsp(args: argparse.Namespace) -> None:
    points = generate_random_points(args.n, seed=args.seed)
    dist_matrix = build_distance_matrix(points)

    t0 = time.time()
    if args.algo == "nn":
        tour = nearest_neighbor_tour(dist_matrix)
        history = None
    elif args.algo == "two_opt":
        tour = nearest_neighbor_tour(dist_matrix)
        tour = two_opt(tour, dist_matrix)
        history = None
    elif args.algo == "sa":
        init = nearest_neighbor_tour(dist_matrix)
        tour, history = simulated_annealing(dist_matrix, init, seed=args.seed)
    elif args.algo == "ga":
        tour, history = genetic_algorithm(
            dist_matrix, generations=args.generations, seed=args.seed
        )
    else:
        raise ValueError(f"Bilinmeyen algoritma: {args.algo}")
    elapsed = time.time() - t0

    length = tour_length(tour, dist_matrix)
    print(f"Algoritma: {args.algo}")
    print(f"Şehir sayısı: {args.n}")
    print(f"Tur uzunluğu: {length:.2f}")
    print(f"Süre: {elapsed:.3f} sn")

    plot_tour(points, tour, title=f"TSP - {args.algo} (uzunluk={length:.1f})", save_path=args.output)
    print(f"Rota görseli kaydedildi: {args.output}")

    if history:
        conv_path = args.output.replace(".png", "_convergence.png")
        plot_convergence(history, save_path=conv_path)
        print(f"Yakınsama grafiği kaydedildi: {conv_path}")


def cmd_vrp(args: argparse.Namespace) -> None:
    points, demands = generate_vrp_instance(args.n, seed=args.seed)
    dist_matrix = build_distance_matrix(points)

    t0 = time.time()
    result = clarke_wright_savings(dist_matrix, demands, vehicle_capacity=args.capacity)
    elapsed = time.time() - t0

    print(f"Müşteri sayısı: {args.n}")
    print(f"Araç kapasitesi: {args.capacity}")
    print(f"Kullanılan araç sayısı: {result.vehicles_used}")
    print(f"Toplam mesafe: {result.total_distance:.2f}")
    print(f"Süre: {elapsed:.3f} sn")
    for i, (route, load, dist) in enumerate(zip(result.routes, result.route_loads, result.route_distances)):
        print(f"  Araç {i + 1}: rota={route} | yük={load:.0f}/{args.capacity} | mesafe={dist:.2f}")

    plot_vrp_routes(points, result.routes, save_path=args.output)
    print(f"VRP rota görseli kaydedildi: {args.output}")


def cmd_compare(args: argparse.Namespace) -> None:
    points = generate_random_points(args.n, seed=args.seed)
    dist_matrix = build_distance_matrix(points)

    results = {}

    nn_tour = nearest_neighbor_tour(dist_matrix)
    results["Nearest Neighbor"] = tour_length(nn_tour, dist_matrix)

    two_opt_tour = two_opt(nn_tour, dist_matrix)
    results["2-opt"] = tour_length(two_opt_tour, dist_matrix)

    sa_tour, _ = simulated_annealing(dist_matrix, nn_tour, seed=args.seed)
    results["Simulated Annealing"] = tour_length(sa_tour, dist_matrix)

    ga_tour, _ = genetic_algorithm(dist_matrix, generations=args.generations, seed=args.seed)
    results["Genetic Algorithm"] = tour_length(ga_tour, dist_matrix)

    print("Sonuçlar:")
    for name, val in results.items():
        print(f"  {name}: {val:.2f}")

    plot_algorithm_comparison(results, save_path=args.output)
    print(f"Karşılaştırma grafiği kaydedildi: {args.output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="routeopt", description="Rota Optimizasyonu Araç Kutusu")
    sub = parser.add_subparsers(dest="command", required=True)

    p_tsp = sub.add_parser("tsp", help="Tek araçlı TSP çöz")
    p_tsp.add_argument("--n", type=int, default=25, help="Şehir sayısı")
    p_tsp.add_argument("--algo", choices=["nn", "two_opt", "sa", "ga"], default="two_opt")
    p_tsp.add_argument("--generations", type=int, default=300, help="GA nesil sayısı")
    p_tsp.add_argument("--seed", type=int, default=None)
    p_tsp.add_argument("--output", default="tour.png")
    p_tsp.set_defaults(func=cmd_tsp)

    p_vrp = sub.add_parser("vrp", help="Kapasiteli çok araçlı VRP çöz")
    p_vrp.add_argument("--n", type=int, default=20, help="Müşteri sayısı")
    p_vrp.add_argument("--capacity", type=float, default=50.0, help="Araç kapasitesi")
    p_vrp.add_argument("--seed", type=int, default=None)
    p_vrp.add_argument("--output", default="vrp_routes.png")
    p_vrp.set_defaults(func=cmd_vrp)

    p_cmp = sub.add_parser("compare", help="Tüm TSP algoritmalarını karşılaştır")
    p_cmp.add_argument("--n", type=int, default=25)
    p_cmp.add_argument("--generations", type=int, default=300)
    p_cmp.add_argument("--seed", type=int, default=None)
    p_cmp.add_argument("--output", default="comparison.png")
    p_cmp.set_defaults(func=cmd_compare)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
