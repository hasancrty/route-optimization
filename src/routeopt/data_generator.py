"""
data_generator.py
-------------------
Test/demo amaçlı rastgele şehir/müşteri verisi üretir ve CSV olarak kaydeder.
"""

from __future__ import annotations

import csv
import random
from typing import List, Tuple


def generate_random_points(
    n: int, width: float = 100.0, height: float = 100.0, seed: int | None = None
) -> List[Tuple[float, float]]:
    rng = random.Random(seed)
    return [(rng.uniform(0, width), rng.uniform(0, height)) for _ in range(n)]


def generate_vrp_instance(
    n_customers: int,
    width: float = 100.0,
    height: float = 100.0,
    min_demand: int = 1,
    max_demand: int = 10,
    seed: int | None = None,
) -> Tuple[List[Tuple[float, float]], List[float]]:
    """Depo (indeks 0, talep=0) + n_customers müşteri üretir."""
    rng = random.Random(seed)
    points = [(width / 2, height / 2)]  # depo merkezde
    demands = [0.0]
    for _ in range(n_customers):
        points.append((rng.uniform(0, width), rng.uniform(0, height)))
        demands.append(float(rng.randint(min_demand, max_demand)))
    return points, demands


def save_points_csv(points: List[Tuple[float, float]], path: str, demands: List[float] | None = None) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["id", "x", "y"] + (["demand"] if demands else [])
        writer.writerow(header)
        for i, (x, y) in enumerate(points):
            row = [i, x, y] + ([demands[i]] if demands else [])
            writer.writerow(row)


def load_points_csv(path: str) -> Tuple[List[Tuple[float, float]], List[float] | None]:
    points: List[Tuple[float, float]] = []
    demands: List[float] = []
    has_demand = False
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        has_demand = "demand" in (reader.fieldnames or [])
        for row in reader:
            points.append((float(row["x"]), float(row["y"])))
            if has_demand:
                demands.append(float(row["demand"]))
    return points, (demands if has_demand else None)
