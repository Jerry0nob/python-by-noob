import math

import numpy as np
import pytest

from matplotlib_basics.charts import (
    format_quadratic,
    plot_dice_rolls,
    plot_quadratic,
    plot_sine,
    quadratic,
    quadratic_roots,
    roll_dice,
)


def test_quadratic_single_value():
    assert quadratic(2, a=3, b=-11, c=8) == -2  # 12 - 22 + 8


def test_quadratic_works_on_numpy_arrays():
    x = np.array([0, 1, 2])
    assert list(quadratic(x, 1, 0, 0)) == [0, 1, 4]


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        ((3, -11, 8), (1.0, 8 / 3)),  # two roots
        ((1, -2, 1), (1.0,)),  # one root: (x - 1)^2
        ((1, 0, 1), ()),  # no real roots: x^2 + 1
    ],
)
def test_quadratic_roots(coefficients, expected):
    roots = quadratic_roots(*coefficients)
    assert len(roots) == len(expected)
    for root, exp in zip(roots, expected):
        assert math.isclose(root, exp)


def test_quadratic_roots_rejects_a_equal_zero():
    with pytest.raises(ValueError):
        quadratic_roots(0, 2, 1)


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        ((3, -11, 8), "f(x) = 3x² - 11x + 8"),
        ((1, 0, -4), "f(x) = 1x² - 4"),
        ((-2, 5, 0), "f(x) = -2x² + 5x"),
    ],
)
def test_format_quadratic(coefficients, expected):
    assert format_quadratic(*coefficients) == expected


def test_roll_dice_is_repeatable_with_seed():
    assert roll_dice(20, seed=7) == roll_dice(20, seed=7)


def test_roll_dice_values_are_valid():
    rolls = roll_dice(1000, seed=1)
    assert len(rolls) == 1000
    assert set(rolls) <= {1, 2, 3, 4, 5, 6}


def test_quadratic_plot_has_labels_and_marked_roots():
    ax = plot_quadratic(3, -11, 8).axes[0]
    assert ax.get_title() == "Quadratic function"
    assert ax.get_xlabel() == "x"
    # 1 line for the function + 1 marker per root
    assert len(ax.get_lines()) >= 3


def test_sine_plot_data_matches_sin():
    line = plot_sine(periods=1).axes[0].get_lines()[0]
    x, y = line.get_data()
    assert np.allclose(y, np.sin(x))


def test_dice_plot_has_one_bar_per_face():
    ax = plot_dice_rolls(roll_dice(60, seed=3)).axes[0]
    assert len(ax.patches) == 6


def test_chart_can_be_saved_as_png(tmp_path):
    path = tmp_path / "sine.png"
    plot_sine().savefig(path)
    assert path.read_bytes()[:4] == b"\x89PNG"
