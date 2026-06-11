# MBE Leaderboard

Auto-generated from `cards/*.json`. Each row is a reproducible KV Compression Card
submitted by PR. **Compare within a (model, budget) group only.**

> Status: **seed / v1.0 in progress.** The numbers below are placeholders showing the
> table shape; they are populated by running `run_mbe.py` on each method. Do **not**
> cite cells marked `—`. Author-reported figures from the literature (survey Table 4)
> are tracked separately in `references/literature_reported.csv` and are **not** mixed
> into this controlled leaderboard.

## Llama-3.1-8B-Instruct — LongBench (avg, ↑)

| Method        | Type           | Full | B50 | B25 | B12 | Training-free |
|---------------|----------------|:----:|:---:|:---:|:---:|:-------------:|
| Full cache    | baseline       |  —   |  —  |  —  |  —  |  —            |
| KIVI          | quantization   |  —   |  —  |  —  |  —  |  ✓            |
| H2O           | eviction       |  —   |  —  |  —  |  —  |  ✓            |
| SnapKV        | eviction       |  —   |  —  |  —  |  —  |  ✓            |
| StreamingLLM  | rolling buffer |  —   |  —  |  —  |  —  |  ✓            |
| PyramidKV     | layer-adaptive |  —   |  —  |  —  |  —  |  ✓            |

## Submit

`run_mbe.py` → `cards/<method>_<model>.json` → PR. CI re-renders this file.
