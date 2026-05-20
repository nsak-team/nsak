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
from matplotlib.patches import Patch

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
        "tool_calls": [],
    },
    "gpt-oss:120b": {
        "duration": [620, 239, 322, 334, 446, 584, 337, 409, 218, 517],
        "tokens": [
            43759,
            48568,
            41534,
            40186,
            15499,
            29928,
            31019,
            23275,
            37287,
            37848,
        ],
        "tool_calls": [3, 11, 3, 4, 6, 8, 7, 6, 6, 11],
    },
    "local": {
        "duration": [615, 677, 284, 232, 338, 636, 660, 282, 619, 359],
        "tokens": [
            22142,
            28161,
            58195,
            28717,
            17437,
            43172,
            49913,
            29714,
            32766,
            20451,
        ],
        "tool_calls": [3, 11, 3, 4, 6, 8, 7, 6, 6, 11],
    },
    "frontier": {
        "duration": [615, 677, 284, 232, 338, 636, 660, 282, 619, 359],
        "tokens": [
            30922,
            20730,
            30849,
            28778,
            35244,
            55136,
            52485,
            39394,
            57053,
            17112,
        ],
        "tool_calls": [3, 11, 3, 4, 6, 8, 7, 6, 6, 11],
    },
}

COLORS = ["#4C72B0", "#DD8452", "#C44E52", "#228B22"]


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
            data["tokens"],
            data["duration"],
            color=color,
            s=60,
            zorder=3,
            label=model,
        )
        if data.get("tool_calls"):
            for x, y, tc in zip(
                data["tokens"], data["duration"], data["tool_calls"], strict=False
            ):
                ax.annotate(
                    f"({tc})",
                    (x, y),
                    textcoords="offset points",
                    xytext=(4, 4),
                    fontsize=7,
                    color=color,
                )

    handles, labels = ax.get_legend_handles_labels()
    handles.append(Patch(color="none", label="tool-calls:()"))
    ax.set_xlabel("Total tokens")
    ax.set_ylabel("Duration (s)")
    ax.legend(handles=handles, fontsize=9)
    ax.grid(alpha=0.35, zorder=0)
    fig.tight_layout()
    _save(fig, "benchmark_tokens_vs_duration" + date)


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
