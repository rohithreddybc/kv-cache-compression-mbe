# KV Compression Card — `<METHOD>` on `<MODEL>`

> Analogous to a Model Card (Mitchell et al., 2019), one card = one method × one model,
> produced by the MBE harness under matched budgets.

- **Method:** `<name>` (`<type: quantization | eviction | merging | architecture | system>`)
- **Model:** `<e.g., Llama-3.1-8B-Instruct (GQA, L=32, H_kv=8)>`
- **Deployment prerequisite:** `<training-free | calibration | pre-training>`
- **Hardware tier:** `<e.g., 1× A100-80GB>`
- **Harness version:** `mbe-vX.Y.Z`

## Accuracy at matched budgets (↑ better)

| Task \ Budget        | Full | B50 | B25 | B12 | B06 |
|----------------------|:----:|:---:|:---:|:---:|:---:|
| Long-doc QA (LongBench) |    |     |     |     |     |
| Multi-hop (RULER)       |    |     |     |     |     |
| Multi-instruction (IFEval) | |     |     |     |     |
| CoT reasoning (GSM8K)   |    |     |     |     |     |
| Agentic / multi-turn    |    |     |     |     |     |

## System metrics (at B25 unless noted)

| Metric                        | Full | Method |
|-------------------------------|:----:|:------:|
| Peak KV memory (GB)           |      |        |
| Decode throughput (tok/s)     |      |        |
| Time-to-first-token (ms)      |      |        |
| Max batch before OOM          |      |        |

## Composability (per survey §8.2)

| Composed with        | Verdict                         | Note |
|----------------------|---------------------------------|------|
| Quantization         | composes / joint-design / conflict |   |
| Eviction / sparsity  | composes / joint-design / conflict |   |
| Paging / offloading  | composes / joint-design / conflict |   |
| GQA / MLA            | composes / joint-design / conflict |   |

## Notes / caveats
`<calibration set, kernel, known failure modes, link to code/commit>`
