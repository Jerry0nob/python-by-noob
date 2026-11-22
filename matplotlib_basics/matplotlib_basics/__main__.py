"""Entry point: python -m matplotlib_basics  -> saves PNG charts to output/"""

from pathlib import Path

from matplotlib_basics.charts import (
    plot_dice_rolls,
    plot_quadratic,
    plot_sine,
    roll_dice,
)

OUTPUT_DIR = Path("output")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    charts = {
        "quadratic.png": plot_quadratic(3, -11, 8),
        "sine.png": plot_sine(),
        "dice.png": plot_dice_rolls(roll_dice(600, seed=42)),
    }
    for name, fig in charts.items():
        path = OUTPUT_DIR / name
        fig.savefig(path, dpi=120)
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
