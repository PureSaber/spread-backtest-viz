"""spread_viz/plots — 图表模块。"""
from __future__ import annotations

from spread_viz.plots.registry import PLOT_REGISTRY, run_compare, run_plots

__all__ = ["PLOT_REGISTRY", "run_plots", "run_compare"]
