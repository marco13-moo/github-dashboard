"""Shared visual style for every dashboard chart."""

from pathlib import Path
from textwrap import shorten

import matplotlib as mpl
import matplotlib.pyplot as plt


CANVAS = "#0d1117"
INK = "#f0f6fc"
MUTED = "#8b949e"
PRIMARY = "#8b5cf6"
PALETTE = [PRIMARY, "#22d3ee", "#34d399", "#fbbf24", "#f472b6", "#60a5fa"]

mpl.rcParams.update(
    {
        "axes.facecolor": CANVAS,
        "axes.labelcolor": MUTED,
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "axes.titlecolor": INK,
        "axes.titlelocation": "left",
        "axes.titlepad": 16,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "figure.facecolor": CANVAS,
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "grid.color": "#30363d",
        "grid.linewidth": 0.8,
        "legend.facecolor": CANVAS,
        "legend.frameon": False,
        "legend.labelcolor": MUTED,
        "savefig.dpi": 160,
        "savefig.facecolor": CANVAS,
        "savefig.pad_inches": 0.18,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
    }
)


_savefig = plt.savefig


def _polish_and_save(filename, *args, **kwargs):
    """Polish the active figure immediately before it is written."""
    figure = plt.gcf()
    for axis in figure.axes:
        axis.set_axisbelow(True)
        bars = [patch for patch in axis.patches if hasattr(patch, "get_width")]
        horizontal = bool(bars) and sum(p.get_width() > p.get_height() for p in bars) > len(bars) / 2
        axis.grid(axis="x" if horizontal else "y", alpha=0.55)
        for side in ("top", "right", "left", "bottom"):
            axis.spines[side].set_visible(False)
        axis.tick_params(length=0, pad=6)

        # Long GitHub names stay readable instead of colliding under the plot.
        if horizontal:
            labels = [shorten(label.get_text(), width=30, placeholder="…") for label in axis.get_yticklabels()]
            axis.set_yticks(axis.get_yticks(), labels=labels)
        elif len(axis.get_xticklabels()) > 6:
            for label in axis.get_xticklabels():
                label.set_rotation(32)
                label.set_horizontalalignment("right")

        # Use a restrained brand color where a chart has one undifferentiated series.
        facecolors = {tuple(p.get_facecolor()) for p in bars}
        if bars and len(facecolors) == 1:
            for patch in bars:
                patch.set_facecolor(PRIMARY)
                patch.set_alpha(0.95)
                patch.set_linewidth(0)

    kwargs.setdefault("bbox_inches", "tight")
    kwargs.setdefault("dpi", 160)
    kwargs.setdefault("facecolor", CANVAS)
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    return _savefig(path, *args, **kwargs)


plt.savefig = _polish_and_save
