"""
Generate benchmark plots for the thesis.

Usage:
    uv run python -m nsak.core.benchmark.benchmark_plot

Output: docs/thesis/documentation/figures/benchmark_*.pdf
"""

import logging
import statistics
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt

FIGURES_DIR = Path(__file__).parents[4] / "docs/thesis/documentation/figures"
date = datetime.now(tz=timezone.utc).strftime("_%d_%m_%Y")
loger = logging.getLogger(__name__)

# ── Data ──────────────────────────────────────────────────────────────────────
# One entry per model. Add new models here.
# Keys are display names used in the legend.

MODELS: dict[str, dict[str, list[int]]] = {
    "recon": {
        "duration": [29, 28, 28, 28, 29, 28, 28, 28, 29, 28],
        "tokens": [],
    },
    "gpt-oss:120b": {
        "duration": [244, 285, 262, 264, 421, 378, 409, 468, 620, 475],
        "tokens": [
            15455,
            15990,
            23152,
            22947,
            31200,
            16768,
            15906,
            23058,
            16159,
            24328,
        ],
    },
    "local": {
        "duration": [310, 340, 290, 380, 450, 400, 360, 420, 510, 395],
        "tokens": [
            13800,
            16700,
            21400,
            20800,
            28000,
            15000,
            14900,
            20600,
            14500,
            21700,
        ],
    },
    "frontier": {
        "duration": [180, 200, 175, 190, 310, 280, 295, 350, 460, 340],
        "tokens": [
            13100,
            15000,
            20200,
            19600,
            26800,
            14300,
            14100,
            19900,
            13900,
            21000,
        ],
    },
}

COLORS = ["#4C72B0", "#DD8452", "#C44E52", "#228B22"]

# ── Plots ─────────────────────────────────────────────────────────────────────


def plot_duration_comparison() -> None:
    """Average duration per model, side by side."""
    names = list(MODELS.keys())
    means = [statistics.mean(MODELS[m]["duration"]) for m in names]

    fig, ax = plt.subplots(figsize=(max(5, len(names)), 4))
    ax.bar(names, means, color=COLORS[: len(names)], zorder=2)
    ax.set_ylabel("Mean Duration (s)")
    ax.set_xlabel("Model")
    ax.grid(axis="y", zorder=0, alpha=0.35)
    fig.tight_layout()
    _save(fig, "benchmark_duration_comparison" + date)


def plot_token_usage() -> None:
    """Average total token usage per model."""
    names = [m for m in MODELS if MODELS[m]["tokens"]]
    means = [statistics.mean(MODELS[m]["tokens"]) for m in names]

    fig, ax = plt.subplots(figsize=(max(5, len(names)), 4))
    ax.bar(names, means, color=COLORS[: len(names)], zorder=2)
    ax.set_ylabel("Mean Total Tokens")
    ax.set_xlabel("Model")
    ax.grid(axis="y", zorder=0, alpha=0.35)
    fig.tight_layout()
    _save(fig, "benchmark_token_usage" + date)


def plot_tokens_vs_duration() -> None:
    """Scatter: total tokens vs. duration, one color per model."""
    fig, ax = plt.subplots(figsize=(7, 4))

    for color, (model, data) in zip(COLORS, MODELS.items(), strict=False):
        if not data["tokens"]:
            continue
        ax.scatter(
            data["tokens"], data["duration"], color=color, s=60, zorder=3, label=model
        )

    ax.set_xlabel("Total tokens")
    ax.set_ylabel("Duration (s)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.35, zorder=0)
    fig.tight_layout()
    _save(fig, "benchmark_tokens_vs_duration" + date)


# ── Save & main ───────────────────────────────────────────────────────────────


def _save(fig: plt.Figure, name: str) -> None:
    """
    Saves the plots in figures.
    """
    path = FIGURES_DIR / f"{name}.pdf"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    info = f"saved {path.relative_to(Path(__file__).parents[4])}"
    loger.info(info)


def create_plots() -> None:
    """
    Creates the plots.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_duration_comparison()
    plot_token_usage()
    plot_tokens_vs_duration()
    loger.info("Done.")


if __name__ == "__main__":
    create_plots()
