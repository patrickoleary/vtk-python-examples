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

## Build the corpus artifact

```bash
python scripts/data/generate_data.py --write --all   # -> data/data.jsonl
```

## Docs site

```bash
cd docs
npm install        # first time only
npm run docs:dev
```
