"""spread_viz/cli.py — 命令行入口。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from spread_viz.config import PLOT_GROUPS, VizConfig
from spread_viz.context import CompareContext, PlotContext
from spread_viz.plots.registry import run_compare, run_plots


def _parse_strategy_params(raw: str | None) -> dict[str, float]:
    if not raw:
        return {}
    out: dict[str, float] = {}
    for part in raw.split(","):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        out[k.strip()] = float(v.strip())
    return out


def _cmd_run(args: argparse.Namespace) -> int:
    plot_group = args.plots
    plot_ids = PLOT_GROUPS.get(plot_group, PLOT_GROUPS["all"])
    cfg = VizConfig(
        output_root=args.output_root,
        run_id=args.run_id,
        out_dir=args.out_dir or str(Path("reports") / args.run_id),
        market_root=args.market_root or "",
        years=list(args.years or []),
        strategy_params=_parse_strategy_params(args.strategy_params),
        top_n=args.top_n,
    )
    ctx = PlotContext.from_run(cfg)
    if ctx.portfolio.empty:
        print(f"警告: {args.run_id} 无 portfolio 数据", file=sys.stderr)
    outputs = run_plots(ctx, plot_ids)
    print(f"已生成 {len(outputs)} 个文件 -> {ctx.out_dir}")
    for p in outputs:
        print(f"  {p.name}")
    return 0


def _cmd_compare(args: argparse.Namespace) -> int:
    if len(args.run_ids) < 2:
        print("compare 至少需要 2 个 run-id", file=sys.stderr)
        return 1
    cfg = VizConfig(
        output_root=args.output_root,
        run_id=args.run_ids[0],
        out_dir=args.out_dir or str(Path("reports") / "compare"),
    )
    runs = [PlotContext.from_run(cfg, rid) for rid in args.run_ids]
    cmp = CompareContext(cfg=cfg, runs=runs, out_dir=Path(cfg.out_dir))
    cmp.out_dir.mkdir(parents=True, exist_ok=True)
    outputs = run_compare(cmp)
    print(f"已生成 {len(outputs)} 个对比图 -> {cmp.out_dir}")
    for p in outputs:
        print(f"  {p.name}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="spread-viz", description="期货价差回测可视化")
    sub = p.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="单 run 生成图表")
    run.add_argument("--output-root", required=True, help="回测 output 根目录")
    run.add_argument("--run-id", required=True, help="run_id 子目录名")
    run.add_argument("--out-dir", default="", help="图表输出目录")
    run.add_argument("--market-root", default="", help="行情 CSV 根目录（图 8）")
    run.add_argument("--years", nargs="*", default=[], help="行情年份，如 2020 2021")
    run.add_argument("--strategy-params", default="", help="lookback=300,entry_z=3.5,exit_z=0.0")
    run.add_argument("--plots", default="all", choices=list(PLOT_GROUPS.keys()))
    run.add_argument("--top-n", type=int, default=10, help="Top/Bottom 套利对数量")
    run.set_defaults(func=_cmd_run)

    cmp = sub.add_parser("compare", help="多 run 对比（图 14）")
    cmp.add_argument("--output-root", required=True)
    cmp.add_argument("--run-ids", nargs="+", required=True)
    cmp.add_argument("--out-dir", default="")
    cmp.set_defaults(func=_cmd_compare)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
