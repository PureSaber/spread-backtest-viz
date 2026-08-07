"""spread_viz/plots/registry.py — 图表注册与批量执行。"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from spread_viz.context import CompareContext, PlotContext
from spread_viz.plots import compare, diagnostic, portfolio, spread, trades

PlotFn = Callable[[PlotContext], Path | list[Path] | None]


def _collect(result: Path | list[Path] | None, acc: list[Path]) -> None:
    if result is None:
        return
    if isinstance(result, list):
        acc.extend(result)
    else:
        acc.append(result)


PLOT_REGISTRY: dict[str, PlotFn] = {
    "01": portfolio.plot_01_nav_drawdown,
    "02": portfolio.plot_02_daily_pnl_dist,
    "03": spread.plot_03_spread_nav,
    "04": portfolio.plot_04_commission_vs_pnl,
    "05": portfolio.plot_05_activity,
    "06": trades.plot_06_roundtrip,
    "07": spread.plot_07_spread_rank,
    "08": diagnostic.plot_08_zscore,
    "09": trades.plot_09_signal_fill,
    "10": diagnostic.plot_10_oi_filter,
    "11": diagnostic.plot_11_roll_events,
    "12": portfolio.plot_12_monthly,
    "13": portfolio.plot_13_rolling,
    "15": spread.plot_15_correlation,
}


def run_plots(ctx: PlotContext, plot_ids: tuple[str, ...]) -> list[Path]:
    outputs: list[Path] = []
    for pid in plot_ids:
        fn = PLOT_REGISTRY.get(pid)
        if fn is None:
            continue
        _collect(fn(ctx), outputs)
    return outputs


def run_compare(ctx: CompareContext) -> list[Path]:
    return compare.plot_14_multi_run(ctx)


__all__ = ["PLOT_REGISTRY", "run_compare", "run_plots"]
