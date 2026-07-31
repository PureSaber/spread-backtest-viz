# spread-backtest-viz

期货价差回测框架产出的可视化工具。只读外部 `output/<run_id>/` 目录，不依赖、不修改回测引擎仓库。

## 环境

```bash
cd D:/projects/spread-backtest-viz
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## 用法

### 单 run：生成 1–15 全部图表

```bash
spread-viz run ^
  --output-root "D:/temp_framework/ver2/future_spread_analysis-team-framework/output" ^
  --run-id baseline_dev ^
  --out-dir "./reports/baseline_dev" ^
  --market-root "D:/data/跨品种" ^
  --years 2020 2021
```

`--market-root` 支持两种目录结构：直接指向含 `MarketData/` 的根目录，或对齐回测 config 的 `data_dir`（会自动探测 `MarketData/` 子目录）。

### 仅 universe 核心图（1–7, 12–15）

```bash
spread-viz run --output-root ... --run-id baseline_dev --plots universe
```

### 多 run 对比（图 14）

```bash
spread-viz compare ^
  --output-root "D:/temp_framework/ver2/future_spread_analysis-team-framework/output" ^
  --run-ids baseline_dev baseline_enhanced_dev ^
  --out-dir "./reports/compare"
```

## 产出图表

| 编号 | 文件前缀 | 说明 |
|------|----------|------|
| 01 | `01_nav_drawdown` | 组合净值 + 回撤 |
| 02 | `02_daily_pnl` | 日盈亏柱 + 活跃日收益分布 |
| 03 | `03_spread_nav` | Top/Bottom 套利对净值 + 月收益热力图 |
| 04 | `04_commission` | 累计手续费 vs 净/毛盈亏 |
| 05 | `05_activity` | 成交笔数 / 活跃套利对数 |
| 06 | `06_roundtrip` | 单笔 round-trip 盈亏与持仓时长 |
| 07 | `07_spread_rank` | 套利对贡献排名与气泡图 |
| 08 | `08_zscore_*` | 价差 + z-score + 买卖点（抽样诊断） |
| 09 | `09_signal_fill` | 信号 vs 成交 |
| 10 | `10_oi_filter` | OI 过滤与有信号无成交 |
| 11 | `11_roll_events` | 换月事件标注（需 `rolls/roll_events.csv`，dom/sub 模式） |
| 12 | `12_monthly` | 月度/年度收益 |
| 13 | `13_rolling` | 滚动 Sharpe / 最大回撤 |
| 14 | `14_multi_run` | 多 run 对比（compare 子命令） |
| 15 | `15_correlation` | 套利对相关性与分散度 |

## 口径说明

- 净值：`1 + cumsum(日收益率)`，加法口径，非复利。
- 组合日收益率：各实例日收益率均值（与回测框架一致）。
- 活跃日：日收益率 ≠ 0 的交易日；分布类图默认用活跃日。

## 测试

```bash
python -m pytest tests/ -q
```
