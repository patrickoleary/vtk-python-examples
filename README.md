# VTK Python Examples

A curated collection of VTK examples in Python with screenshots and documentation.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Node.js 18+

## Setup

```bash
uv sync
cd docs && npm install
```

## Running Tests

```bash
uv run python -m pytest src/tests/test_examples.py -v -s
```

## Adding a New Example

1. Create `src/Python/{Category}/{Title}.py`
2. Create `src/Python/{Category}/{Title}.md` (companion description)
3. Add an entry to `src/tests/test_manifest.json`
4. Run the tests to generate a screenshot
5. Rebuild the docs

## Rebuilding the Docs

From the `docs/` directory:

```bash
npm run publish
```

This single command:

1. Regenerates all pages, sidebar, gallery, images, and JSONL from `test_manifest.json`
2. Builds the static VitePress site
3. Serves it locally for preview

## Project Structure

```
src/
  Python/{Category}/{Title}.py    # Example scripts
  Python/{Category}/{Title}.md    # Companion descriptions
  tests/test_manifest.json        # Single source of truth for all examples
  tests/test_examples.py          # Test harness
scripts/
  generate_examples_jsonl.py      # Generates all doc artifacts
data/
  examples.jsonl                  # Full dataset (JSONL)
  images/testing/                 # Test screenshots
docs/
  .vitepress/config.mjs           # VitePress config
  .vitepress/generated/           # Auto-generated sidebar and gallery data
  examples/                       # Auto-generated per-example pages
  public/images/                  # Auto-generated screenshot copies
```
