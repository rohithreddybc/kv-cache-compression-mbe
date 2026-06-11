# Contributing a result to MBE

MBE grows by accumulating reproducible KV Compression Cards. To add yours:

1. **Implement an adapter** in `methods/<yourmethod>.py` subclassing
   `methods.base.KVCompressor` (see `methods/kivi.py` for the pattern). You only
   implement `set_budget()` and `wrap()`.
2. **Write a config** in `configs/<yourmethod>.yaml` (copy `example_method.yaml`).
3. **Run the harness** on the required model suite:
   ```bash
   python run_mbe.py --config configs/<yourmethod>.yaml --out cards/<method>_<model>.json
   ```
4. **Open a pull request** adding the `cards/*.json`. CI validates the schema,
   re-renders the card to Markdown, and regenerates `LEADERBOARD.md`.

## Rules that keep results comparable

- Report at the fixed budgets **B50 / B25 / B12** (B06 optional). Do not invent budgets.
- Use the **declared model suite**; if you add a model, add it for the full suite.
- Always report the **system metrics**, not accuracy alone.
- State your **deployment prerequisite** and **composability** honestly.
- Pin your code commit and calibration set in the card `notes`.

Author-reported numbers lifted from papers go in `references/literature_reported.csv`,
**not** in the controlled leaderboard, because they are not matched-budget.
