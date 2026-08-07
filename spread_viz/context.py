"""spread_viz/context.py — 绘图上下文。"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from spread_viz.config import VizConfig
from spread_viz.loader import load_run
from spread_viz.metrics import net_value_from_pct, spread_cumulative_pnl
from spread_viz.pairing import pair_roundtrips


@dataclass
class PlotContext:
    cfg: VizConfig
    run_id: str
    run_dir: Path
    portfolio: pd.DataFrame
    symbol: pd.DataFrame
    trades: pd.DataFrame
    signals: pd.DataFrame
    rolls: pd.DataFrame
    summary: pd.DataFrame
    out_dir: Path
    roundtrips: pd.DataFrame = field(default_factory=pd.DataFrame)
    spread_pnl: pd.Series = field(default_factory=lambda: pd.Series(dtype=float))

    @classmethod
    def from_run(cls, cfg: VizConfig, run_id: str | None = None) -> PlotContext:
        rid = run_id or cfg.run_id
        data = load_run(cfg.output_root, rid)
        port = data["portfolio"]
        if not port.empty and "net_value" not in port.columns:
            port = port.copy()
            port["net_value"] = net_value_from_pct(port["daily_pnl_pct"])
        sym = data["symbol"]
        trades = data["trades"]
        rt = pair_roundtrips(trades)
        pnl = spread_cumulative_pnl(sym) if not sym.empty else pd.Series(dtype=float)
        out = Path(cfg.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        return cls(
            cfg=cfg,
            run_id=rid,
            run_dir=Path(data["run_dir"]),
            portfolio=port,
            symbol=sym,
            trades=trades,
            signals=data["signals"],
            rolls=data["rolls"],
            summary=data["summary"],
            out_dir=out,
            roundtrips=rt,
            spread_pnl=pnl,
        )


@dataclass
class CompareContext:
    cfg: VizConfig
    runs: list[PlotContext]
    out_dir: Path


__all__ = ["CompareContext", "PlotContext"]
