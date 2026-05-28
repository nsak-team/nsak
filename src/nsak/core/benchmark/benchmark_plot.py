"""
Generate benchmark plots for the thesis.

Usage:
    uv run python -m nsak.core.benchmark.benchmark_plot path/to/a.json path/to/b.json ...

Output: docs/thesis/documentation/figures/benchmark_*.pdf
"""

import argparse
import json
import logging
import math
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter, ScalarFormatter

logging.getLogger("matplotlib").setLevel(logging.WARNING)

FIGURES_DIR = Path(__file__).parents[4] / "docs/thesis/documentation/figures"
date = datetime.now(tz=timezone.utc).strftime("_%d_%m_%Y")
loger = logging.getLogger(__name__)

MODELS: dict[str, dict] = {}  # type: ignore

COLORS = ["#C3ACCE", "#89909F", "#C76E00", "#538083"]
COLORS_FINDING = ["#5AB1BB", "#A5C882", "#F7DD72", "#4E6766"]


# ── Loader ────────────────────────────────────────────────────────────────────


def load_json(path: Path) -> None:
    """
    Load the json.
    """
    data = json.loads(path.read_text())
    MODELS[data["model"]] = {
        "durations": data["durations"],
        "tokens": data["tokens"],
        "tool_calls": data["tool_calls"],
        "mean_duration": data["mean_duration"],
        "mean_tokens": data["mean_tokens"],
        "mean_tool_calls": data.get("mean_tool_calls"),
        "mean_hosts_discovered": data.get("mean_hosts_discovered"),
        "mean_services_discovered": data.get("mean_services_discovered"),
        "mean_findings": data.get("mean_findings"),
    }


def plot_duration_comparison() -> None:
    """Mean duration per model, side by side."""
    names = list(MODELS.keys())
    means = [MODELS[m]["mean_duration"] for m in names]

    fig, ax = plt.subplots(figsize=(max(5, math.floor(len(names) * 1.5)), 4))
    ax.bar(names, means, color=COLORS[: len(names)], zorder=2)
    ax.ticklabel_format(style="plain", axis="y")
    ax.set_ylabel("Mean Duration (s)")
    ax.set_xlabel("Claude-Opus-4.7")
    ax.grid(axis="y", zorder=0, alpha=0.35)
    fig.tight_layout()
    _save(fig, "benchmark_duration_comparison" + date)


def plot_token_usage() -> None:
    """Mean total token usage per model."""
    names = [m for m in MODELS if MODELS[m].get("mean_tokens") is not None]
    means = [MODELS[m]["mean_tokens"] for m in names]

    fig, ax = plt.subplots(figsize=(max(5, len(names)), 4))
    ax.bar(names, means, color=COLORS[: len(names)], zorder=2)
    ax.ticklabel_format(style="plain", axis="y")
    ax.set_ylabel("Mean Total Tokens")
    ax.set_xlabel("Claude-Opus-4.7")
    ax.grid(axis="y", zorder=0, alpha=0.35)
    fig.tight_layout()
    _save(fig, "benchmark_token_usage" + date)


def plot_services() -> None:
    """Mean hosts, services, and findings per model as grouped bars."""
    names = [m for m in MODELS if MODELS[m].get("mean_hosts_discovered") is not None]
    if not names:
        return

    host_vals = [MODELS[m]["mean_hosts_discovered"] for m in names]
    service_vals = [MODELS[m]["mean_services_discovered"] for m in names]
    finding_vals = [MODELS[m]["mean_findings"] for m in names]

    x = np.arange(len(names))
    width = 0.25

    fig, ax = plt.subplots(figsize=(max(5, math.floor(len(names) * 1.5)), 4))
    bars1 = ax.bar(
        x - width,
        host_vals,
        width,
        label="Avg. Hosts",
        color=COLORS_FINDING[0],
        zorder=2,
    )
    bars2 = ax.bar(
        x, service_vals, width, label="Avg. Services", color=COLORS_FINDING[1], zorder=2
    )
    bars3 = ax.bar(
        x + width,
        finding_vals,
        width,
        label="Avg. Findings",
        color=COLORS_FINDING[2],
        zorder=2,
    )

    ax.bar_label(bars1, padding=3)
    ax.bar_label(bars2, padding=3)
    ax.bar_label(bars3, padding=3)

    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.ticklabel_format(style="plain", axis="y")
    ax.set_ylabel("Count")
    ax.set_xlabel("Claude-Opus-4.7")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.legend(loc="upper left")
    ax.grid(axis="y", zorder=0, alpha=0.35)
    fig.tight_layout()
    _save(fig, "benchmark_services" + date)


def plot_tokens_vs_duration() -> None:
    """Scatter: total tokens vs. duration, one color per model."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xscale("log")
    ax.set_yscale("log")
    _k_fmt = FuncFormatter(
        lambda v, _: f"{int(v / 1000)}k" if v >= 5000 else str(int(v))
    )
    ax.xaxis.set_major_locator(LogLocator(base=10, subs=[1, 2, 3, 4, 5, 6, 7]))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs=[]))
    ax.xaxis.set_major_formatter(_k_fmt)
    ax.xaxis.set_minor_formatter(NullFormatter())
    _plain_fmt = FuncFormatter(lambda v, _: str(int(v)))
    ax.yaxis.set_major_locator(LogLocator(base=10, subs=[1, 2, 3]))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=[]))
    ax.yaxis.set_major_formatter(_plain_fmt)
    ax.yaxis.set_minor_formatter(NullFormatter())

    for color, (model, data) in zip(COLORS, MODELS.items(), strict=False):
        mean_tc = data["mean_tool_calls"] if data["tool_calls"] else None
        label = (
            f"{model} (avg. {mean_tc:.1f} tool calls)" if mean_tc is not None else model
        )
        if data["tokens"]:
            ax.scatter(
                data["tokens"],
                data["durations"],
                color=color,
                s=60,
                zorder=3,
                label=label,
            )
            if data["tool_calls"]:
                for x, y, tc in zip(
                    data["tokens"], data["durations"], data["tool_calls"], strict=False
                ):
                    ax.annotate(
                        f"({tc})",
                        (x, y),
                        textcoords="offset points",
                        xytext=(4, 4),
                        fontsize=7,
                        color=color,
                    )
        if data["mean_duration"] is not None:
            ax.axhline(
                data["mean_duration"],
                color=color,
                linestyle="--",
                linewidth=1.2,
                label=label if not data["tokens"] else None,
            )

    handles, _ = ax.get_legend_handles_labels()
    handles.append(Patch(color="none", label="( ) = tool calls per run"))
    ax.set_xlabel("Total tokens")
    ax.set_ylabel("Duration (s)")
    ax.legend(handles=handles, fontsize=9, loc="lower right")
    ax.grid(alpha=0.35, zorder=0)
    fig.tight_layout()
    _save(fig, "benchmark_tokens_vs_duration" + date)


# ── Save & main ───────────────────────────────────────────────────────────────


def _save(fig: plt.Figure, name: str) -> None:
    path = FIGURES_DIR / f"{name}.svg"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    loger.info("saved %s", path.relative_to(Path(__file__).parents[4]))


def create_plots() -> None:
    """
    Create the plots.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_duration_comparison()
    plot_token_usage()
    plot_tokens_vs_duration()
    plot_services()
    loger.info("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_paths", type=Path, nargs="+")
    args = parser.parse_args()
    for json_path in args.json_paths:
        load_json(json_path)
    create_plots()
