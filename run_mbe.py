#!/usr/bin/env python3
"""
MBE harness (skeleton) — Matched-Budget Evaluation for KV cache compression.

Config-driven entry point. It sweeps a method across the fixed MBE budget ladder,
runs the standardized task suite, collects system metrics, and emits one
KV Compression Card as JSON.

This is a reference skeleton: the task runners and the model/serving hooks are
intentionally pluggable (`methods/base.py`, `tasks/`). Fill in an adapter for your
method and a backend for your serving stack, then:

    python run_mbe.py --config configs/example_method.yaml --out cards/mymethod.json
"""
from __future__ import annotations
import argparse
import json
import importlib

# Fixed MBE budget ladder (retained KV fraction). Section 10.1 of the paper.
MBE_BUDGETS = {"B50": 0.50, "B25": 0.25, "B12": 0.125, "B06": 0.0625}

# Required task suite (Section 10.2 / Table 5). Each maps to a runner in tasks/.
MBE_TASKS = [
    "longbench",       # long-document retrieval / QA
    "ruler",           # multi-hop tracing + aggregation
    "ifeval",          # multi-instruction following
    "gsm8k",           # chain-of-thought reasoning (compression-sensitive)
    "agentic_trace",   # >=1 long-horizon / multi-turn trace
]

# Required system metrics (Section 10.2).
MBE_SYSTEM_METRICS = [
    "peak_kv_memory_gb",
    "decode_throughput_tok_s",
    "ttft_ms",
    "max_batch_before_oom",
]


def load_yaml(path):
    import yaml  # pyyaml
    with open(path) as f:
        return yaml.safe_load(f)


def load_compressor(spec):
    """spec: {module: 'methods.kivi', class: 'KIVICompressor', args: {...}}"""
    mod = importlib.import_module(spec["module"])
    cls = getattr(mod, spec["class"])
    return cls(**spec.get("args", {}))


def evaluate(cfg):
    compressor = load_compressor(cfg["method"])
    model_id = cfg["model"]["id"]
    optional = set(cfg.get("optional_budgets", []))
    budgets = {k: v for k, v in MBE_BUDGETS.items()
               if k != "B06" or "B06" in optional}

    card = {
        "method": cfg["method"]["name"],
        "type": cfg["method"]["type"],
        "model": model_id,
        "attention": cfg["model"].get("attention", "unknown"),
        "prerequisite": cfg["method"].get("prerequisite", "unknown"),
        "hardware_tier": cfg.get("hardware_tier", "unspecified"),
        "harness_version": "mbe-0.1.0",
        "accuracy": {},   # task -> {budget -> score}
        "system": {},     # budget -> {metric -> value}
        "composability": cfg["method"].get("composability", {}),
        "notes": cfg.get("notes", ""),
    }

    # full-cache reference
    card["accuracy"]["full"] = {t: run_task(t, compressor, model_id, budget=1.0)
                                for t in MBE_TASKS}

    for name, frac in budgets.items():
        compressor.set_budget(frac)
        card["accuracy"][name] = {t: run_task(t, compressor, model_id, budget=frac)
                                  for t in MBE_TASKS}
        card["system"][name] = collect_system_metrics(compressor, model_id)

    return card


def run_task(task, compressor, model_id, budget):
    """Dispatch to tasks/<task>.py:run(...). Returns a float score.
    Skeleton: integrate your eval backend (lm-eval-harness, LongBench, RULER, ...)."""
    runner = importlib.import_module(f"tasks.{task}")
    return runner.run(compressor=compressor, model_id=model_id, budget=budget)


def collect_system_metrics(compressor, model_id):
    """Skeleton hook — wire to your serving backend (vLLM/SGLang/TensorRT-LLM)."""
    return {m: None for m in MBE_SYSTEM_METRICS}


def main():
    ap = argparse.ArgumentParser(description="Run Matched-Budget Evaluation.")
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    cfg = load_yaml(args.config)
    card = evaluate(cfg)
    with open(args.out, "w") as f:
        json.dump(card, f, indent=2)
    print(f"Wrote card -> {args.out}")


if __name__ == "__main__":
    main()
