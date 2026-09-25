import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from routeopt.algorithms import genetic_algorithm, nearest_neighbor_tour, simulated_annealing, two_opt
from routeopt.data_generator import generate_random_points, generate_vrp_instance
from routeopt.distance import build_distance_matrix, tour_length
from routeopt.vrp import clarke_wright_savings


def _valid_permutation(tour, n):
    return sorted(tour) == list(range(n))


def test_nearest_neighbor_visits_all_cities():
    points = generate_random_points(15, seed=1)
    dm = build_distance_matrix(points)
    tour = nearest_neighbor_tour(dm)
    assert _valid_permutation(tour, 15)


def test_two_opt_improves_or_equals_nn():
    points = generate_random_points(20, seed=2)
    dm = build_distance_matrix(points)
    nn_tour = nearest_neighbor_tour(dm)
    improved = two_opt(nn_tour, dm)
    assert _valid_permutation(improved, 20)
    assert tour_length(improved, dm) <= tour_length(nn_tour, dm) + 1e-6


def test_simulated_annealing_valid_and_improves():
    points = generate_random_points(20, seed=3)
    dm = build_distance_matrix(points)
    nn_tour = nearest_neighbor_tour(dm)
    sa_tour, history = simulated_annealing(dm, nn_tour, seed=3)
    assert _valid_permutation(sa_tour, 20)
    assert tour_length(sa_tour, dm) <= tour_length(nn_tour, dm) + 1e-6
    assert history[-1] <= history[0] + 1e-6


def test_genetic_algorithm_valid_tour():
    points = generate_random_points(15, seed=4)
    dm = build_distance_matrix(points)
    ga_tour, history = genetic_algorithm(dm, population_size=30, generations=50, seed=4)
    assert _valid_permutation(ga_tour, 15)
    assert history[-1] <= history[0] + 1e-6


def test_vrp_respects_capacity():
    points, demands = generate_vrp_instance(20, min_demand=5, max_demand=15, seed=5)
    dm = build_distance_matrix(points)
    capacity = 40
    result = clarke_wright_savings(dm, demands, vehicle_capacity=capacity)

    # Tüm müşteriler tam olarak bir kez ziyaret edilmeli
    all_customers = sorted(c for route in result.routes for c in route)
    expected = list(range(1, 21))  # depo = 0
    assert all_customers == expected

    # Kapasite aşılmamalı
    for load in result.route_loads:
        assert load <= capacity + 1e-6
