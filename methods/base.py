"""Adapter interface every MBE method implements.

A method only has to expose how to apply itself at a given retained-KV budget;
the harness owns the budget ladder, task running, and metric collection.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class KVCompressor(ABC):
    name: str = "unnamed"
    type: str = "unknown"  # quantization | eviction | merging | architecture | system

    @abstractmethod
    def set_budget(self, retained_fraction: float) -> None:
        """Configure the method to retain `retained_fraction` of the full KV footprint
        (e.g., 0.25 for B25). Implementations map this to bit-width, token budget,
        page count, etc."""
        ...

    @abstractmethod
    def wrap(self, model):
        """Return a model/attention object with this compression applied, ready for
        the task runners. Implementations hook their kernels/eviction here."""
        ...

    def composability(self) -> dict:
        """Optional: declare composition verdicts vs other families (survey §8.2)."""
        return {}


class FullCacheBaseline(KVCompressor):
    name = "full-cache"
    type = "baseline"

    def set_budget(self, retained_fraction: float) -> None:
        self._frac = retained_fraction

    def wrap(self, model):
        return model
