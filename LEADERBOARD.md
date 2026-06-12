# MBE Leaderboard

Auto-generated from `cards/*.json`. Each row is a reproducible KV Compression Card.
**Compare within a (model, budget) group only.**

---

## Proof-of-concept run (CPU smoke test) — REAL numbers

> Produced by `eval/smoke_quant.py` on **Qwen2.5-0.5B-Instruct (GQA), CPU/float32**,
> passkey retrieval, N=10. This is a **proof-of-concept that the harness runs
> end-to-end and produces matched-budget numbers** — it is **not** the paper's 7-8B
> suite. KV quantization is KIVI-style (per-channel keys, per-token values), applied to
> the prefill cache.

| Method  | KV budget | Passkey accuracy |
|---------|:---------:|:----------------:|
| full-FP |   100%    |       1.00       |
| KV-8bit |   50%     |       1.00       |
| KV-4bit |   25%     |       1.00       |
| KV-2bit |   12.5%   |     **0.00**     |

**Finding:** 8-bit and 4-bit KV quantization are lossless on this task; **2-bit
collapses** (model emits garbage). This reproduces, at small scale, the well-documented
2-bit KV fragility (cf. the survey's §4.1.3 and Chen et al. 2025a).

---

## Full suite (seed) — in progress

> Status: **placeholder.** Populate by running `run_mbe.py` for the methods below on a
> 7-8B model across the 50/25/12.5% budget ladder (a single-GPU job). Cells marked `—`
> are not yet measured; **do not cite `—` cells.** Author-reported literature numbers
> live in the survey's Table 5, not here.

### Llama-3.1-8B-Instruct — LongBench (avg, ↑)

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
