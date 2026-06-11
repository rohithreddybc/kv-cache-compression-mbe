"""Reference task runner stub: LongBench (long-document retrieval / QA).

Pattern for all task runners: expose `run(compressor, model_id, budget) -> float`.
Wire to your eval backend (e.g., the official LongBench scripts or lm-eval).
"""


def run(compressor, model_id: str, budget: float) -> float:
    """Return an average LongBench score for `model_id` under `compressor` at
    `budget` retained KV fraction. Skeleton returns None until wired."""
    model = compressor.wrap(_load_model(model_id))
    # TODO: run LongBench subtasks with `model`, average the scores.
    return None


def _load_model(model_id):
    # TODO: load via your backend (transformers / vLLM).
    return None
