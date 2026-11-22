"""Small math helpers and the charts built from them."""

import math
import random
from collections import Counter

import numpy as np
from matplotlib.figure import Figure


def quadratic(x, a: float, b: float, c: float):
    """Return a*x^2 + b*x + c. Works for a single number or a numpy array."""
    return a * x**2 + b * x + c


def quadratic_roots(a: float, b: float, c: float) -> tuple[float, ...]:
    """Return the real roots of a*x^2 + b*x + c = 0, smallest first."""
    if a == 0:
        raise ValueError("'a' must not be 0, otherwise it is not a quadratic")
    delta = b**2 - 4 * a * c
    if delta < 0:
        return ()
    if delta == 0:
        return (-b / (2 * a),)
    root1 = (-b - math.sqrt(delta)) / (2 * a)
    root2 = (-b + math.sqrt(delta)) / (2 * a)
    return tuple(sorted((root1, root2)))


def format_quadratic(a: float, b: float, c: float) -> str:
    """Return a readable formula, e.g. 'f(x) = 3x² - 11x + 8'."""
    formula = f"{a:g}x²"
    for value, suffix in ((b, "x"), (c, "")):
        if value:
            sign = "-" if value < 0 else "+"
            formula += f" {sign} {abs(value):g}{suffix}"
    return f"f(x) = {formula}"


def plot_quadratic(a: float, b: float, c: float, x_min=-2.0, x_max=6.0) -> Figure:
    """Plot the quadratic function and mark its roots."""
    x = np.linspace(x_min, x_max, 400)
    fig = Figure(figsize=(7, 4.5))
    ax = fig.subplots()
    ax.plot(
        x,
        quadratic(x, a, b, c),
        color="tab:blue",
        linewidth=2,
        label=format_quadratic(a, b, c),
    )
    for root in quadratic_roots(a, b, c):
        ax.plot(root, 0, "o", color="tab:red")
        ax.annotate(
            f"x = {root:.2f}", (root, 0), textcoords="offset points", xytext=(5, 10)
        )
    ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
    ax.axvline(0, color="black", linewidth=0.5, linestyle="--")
    ax.set(title="Quadratic function", xlabel="x", ylabel="f(x)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_sine(periods: int = 2) -> Figure:
    """Plot sin(x) over the given number of full periods."""
    x = np.linspace(0, periods * 2 * np.pi, 300)
    fig = Figure(figsize=(7, 4))
    ax = fig.subplots()
    ax.plot(x, np.sin(x), color="tab:green")
    ax.set(title="Sine wave", xlabel="x [rad]", ylabel="sin(x)")
    ax.grid(True, linestyle=":", alpha=0.6)
    fig.tight_layout()
    return fig


def roll_dice(count: int, seed: int | None = None) -> list[int]:
    """Roll a six-sided die `count` times. The same seed gives the same rolls."""
    rng = random.Random(seed)
    return [rng.randint(1, 6) for _ in range(count)]


def plot_dice_rolls(rolls: list[int]) -> Figure:
    """Bar chart: how many times each face of the die came up."""
    counts = Counter(rolls)
    faces = list(range(1, 7))
    fig = Figure(figsize=(7, 4))
    ax = fig.subplots()
    ax.bar(faces, [counts[face] for face in faces], color="tab:orange")
    ax.axhline(
        len(rolls) / 6, color="black", linestyle="--", label="expected (fair die)"
    )
    ax.set(
        title=f"{len(rolls)} dice rolls", xlabel="Face", ylabel="Count", xticks=faces
    )
    ax.margins(y=0.25)  # free space above the bars for the legend
    ax.legend(loc="upper center")
    fig.tight_layout()
    return fig
