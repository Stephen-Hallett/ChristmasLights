import math
from random import uniform

from matplotlib import figure
from matplotlib import pyplot as plt
from matplotlib.colors import to_rgb

from .utilities import load_streamlit_config


def get_sparkle(proportion: float = 0):
    return int(uniform(0, 1) >= proportion)


def make_tree(
    n: int, pattern: list[str], alpha: int = 1, sparkle: int = 0
) -> figure.Figure:
    rows = []
    gaps = []

    i = 0
    while sum(rows) < n:
        rows.append(i * 2)
        i += 1

    base_colours = (pattern * math.ceil(sum(rows) / len(pattern)))[: sum(rows)]

    colours = [
        (*to_rgb(colour), get_sparkle(sparkle) * alpha) for colour in base_colours
    ]

    gaps = [(max(rows) - item) / 2 for item in rows]

    inverse_rows = rows[::-1]

    points = [
        (j + gaps[i], inverse_rows[i] + (1 - j / row))
        for i, row in enumerate(rows)
        for j in range(row)
    ]

    points = points[::-1]

    x, y = zip(*points, strict=False)

    fig, ax = plt.subplots(
        figsize=(6, 8), facecolor=load_streamlit_config()["theme"]["backgroundColor"]
    )
    ax.axis("off")

    triangle_x = [-2, (max(rows) + min(gaps) - 1) / 2, max(rows)]  # Base, peak, base
    triangle_y = [-1, max(rows) + 2, -1]  # Bottom left, top center, bottom right
    ax.fill(triangle_x, triangle_y, color="green", alpha=0.7)
    ax.axis("off")
    ax.margins(0)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.scatter(x, y, c=colours)
    return fig
