# spread-backtest-viz

> **Deprecated (v0.2.0)** — This repo is a thin compatibility shim. All visualization logic lives in **[quant-report-hub](../quant-report-hub)**. Prefer `quant-report run --adapter spread` or install `quant-report-hub` and use its `spread-viz` entry point.

期货价差回测框架产出的可视化工具（**已合并至 quant-report-hub**）。本仓库仅保留旧 CLI `spread-viz` 以兼容既有脚本。

## 迁移

```bash
# 推荐：安装 hub
cd ../quant-report-hub
pip install -e ".[dev]"

quant-report run ^
  --adapter spread ^
  --output-root "D:/path/to/output" ^
  --run-id baseline_dev ^
  --out-dir "./reports/baseline_dev"
```

旧命令仍可用（会显示 `DeprecationWarning`）：

```bash
pip install -e ../quant-report-hub
pip install -e .
spread-viz run --output-root ... --run-id baseline_dev
```

## 图表说明

完整 01–15 图表说明见 [quant-report-hub README](../quant-report-hub/README.md)（spread 模式与原先一致）。

## 归档计划

见 [quant-report-hub/docs/MERGE_PLAN.md](../quant-report-hub/docs/MERGE_PLAN.md) Phase 3 — 本仓库将在迁移完成后 **GitHub archive**（只读，不删除历史）。

## 测试

```bash
pip install -e ../quant-report-hub
pip install -e ".[dev]"
pytest -q
```
