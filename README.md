# spread-backtest-viz

> **Deprecated (v0.2.0)** — This repo is a thin compatibility shim. All visualization logic lives in **[quant-report-hub](https://github.com/PureSaber/quant-report-hub)**. Prefer `quant-report run --adapter spread` or install `quant-report-hub` and use its `spread-viz` entry point.

期货价差回测框架产出的可视化工具（**已合并至 quant-report-hub**）。本仓库仅保留旧 CLI `spread-viz` 以兼容既有脚本。

## 迁移

```bash
# 推荐：直接安装canonical hub
python -m pip install "quant-report-hub @ git+https://github.com/PureSaber/quant-report-hub.git@b334b34a61f6e563916add32af94d70dc7ed7494"

quant-report run ^
  --adapter spread ^
  --output-root "D:/path/to/output" ^
  --run-id baseline_dev ^
  --out-dir "./reports/baseline_dev"
```

旧命令仍可用（会显示 `DeprecationWarning`）：

```bash
python -m pip install -e ".[dev]"
spread-viz run --output-root ... --run-id baseline_dev
```

## 图表说明

完整01–15图表说明见[quant-report-hub README](https://github.com/PureSaber/quant-report-hub#readme)（spread模式与原先一致）。

## 归档计划

见[quant-report-hub/docs/MERGE_PLAN.md](https://github.com/PureSaber/quant-report-hub/blob/main/docs/MERGE_PLAN.md) Phase 3。本仓库完成最终绿色CI、恢复锚点和治理文档同步后将执行**GitHub archive**；归档只把仓库设为只读，不删除Git历史。

本shim不发布到PyPI。为避免浮动依赖和不可解析的包索引，`pyproject.toml`固定到已通过CI和CodeQL的canonical commit`b334b34a61f6e563916add32af94d70dc7ed7494`。归档后新项目只应直接使用`quant-report-hub`。

## 测试

```bash
pip install -e ".[dev]"
pytest -q
```
