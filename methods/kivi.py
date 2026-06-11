"""Reference adapter stub: KIVI (per-channel key / per-token value quantization).

Demonstrates the adapter pattern. Wire `wrap()` to your KIVI kernel and
`set_budget()` to the bit-width that realises each retained fraction.
"""
from .base import KVCompressor


class KIVICompressor(KVCompressor):
    name = "KIVI"
    type = "quantization"

    def __init__(self, key_bits_per_budget=None, **kw):
        self.key_bits_per_budget = key_bits_per_budget or {"B50": 8, "B25": 4, "B12": 2}
        self._bits = 16

    def set_budget(self, retained_fraction: float) -> None:
        # 16-bit baseline; bit-width ~ 16 * retained_fraction (per element).
        self._bits = max(2, round(16 * retained_fraction))

    def wrap(self, model):
        # TODO: attach KIVI quantized-attention kernel at self._bits bits
        #       (per-channel keys, per-token values). Returns the wrapped model.
        return model

    def composability(self):
        return {"eviction": "joint-design", "paging": "composes", "gqa_mla": "composes"}
