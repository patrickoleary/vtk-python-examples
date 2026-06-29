# VTK Python Examples

The VTK Python example corpus and its gallery website. Split out from
`vtk-ontology`; the two repos exchange data via GitHub release artifacts.

## Layout

- `docs/public/examples/{tag}/{name}.{py,json,png}` — the example corpus
  (source, sidecar metadata, rendered image) + `examples/data/` shared datasets.
- `scripts/data/generate_data.py` — build `data/data.jsonl` (corpus artifact
  consumed by the `vtk-ontology` parser).
- `docs/` — VitePress site: landing page, gallery, per-example/tag pages.

## Data exchange (release artifacts)

- **Publish** `data.jsonl` ← built here, consumed by `vtk-ontology`.
- **Consume** `experiments.jsonl` ← built by `vtk-ontology`, drives the DSL/event
  sections on example pages. Fetched (pinned) into `vendor/`.

The consumed artifact is declared in `artifacts.lock.json`; edit its `source`
to point at a local path (now) or a GitHub release asset URL (later).

```bash
# Fetch experiments.jsonl into vendor/ (verifies pinned sha256)
python -m scripts.artifacts.fetch_artifacts
# Re-pin after the upstream artifact changes
python -m scripts.artifacts.fetch_artifacts --update
```

## Full build sequence

```bash
# 1. Build the corpus artifact published for vtk-ontology
python scripts/data/generate_data.py --write --all      # -> data/data.jsonl

# 2. Fetch the experiments artifact produced by vtk-ontology
python -m scripts.artifacts.fetch_artifacts             # -> vendor/experiments.jsonl

# 3. Generate the site pages from corpus + experiments.jsonl
python -m scripts.web.generate_site                     # -> docs/index.md, docs/examples/, sidebar, gallery

# 4. Run the docs site
cd docs && npm install && npm run docs:dev              # npm install first time only
```

## Running examples interactively

```bash
# Run an example from the corpus
./ex annotation/axis_actor2d.py
# or
uv run scripts/utils/run_example.py annotation/axis_actor2d.py
```

The `ex` script is a convenience wrapper that sets `VPE_DATA_DIR` to point at the shared datasets in `docs/public/examples/data/`.

## Testing

The `tests/` directory contains a screenshot regression test harness:

```bash
# Generate the test manifest from the corpus
uv run python tests/generate_data_manifest.py

# Run all tests
uv run python tests/test_examples.py

# Run tests for a specific tag
uv run python tests/test_examples.py --tag annotation

# Run tests matching a name substring
uv run python tests/test_examples.py --name axis_actor
```

Tests run examples offscreen, capture screenshots, and compare them against reference images using SSIM (threshold 0.995). Results are written to `tests/results.csv`.
