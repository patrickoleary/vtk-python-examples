# Contributing

The goal of this project is to teach VTK pipelines through Python, not to teach Python itself. Examples intentionally avoid object-oriented patterns, helper functions, refactoring, and other software engineering practices. Each example focuses on one thing: how to assemble a specific VTK pipeline. Users are free to adapt the code to their own style — but the examples themselves stay simple and explicit.

There is no prescribed reading order. Every example assumes the reader has never seen another example in this collection. That means every example is fully self-contained: explicit imports, no shared utilities, and comments on each pipeline stage.

## What each example requires

1. `src/Python/{Category}/{Title}.py` — the example script
2. `src/Python/{Category}/{Title}.md` — companion description
3. An entry in `src/tests/test_manifest.json`

## Python file standards

Every `.py` file must follow the conventions shown in `Arrow.py`:

- **Standalone** — each example is a complete, runnable script. No helper functions, no utility modules, no shared imports across examples.
- **Standard VTK pipeline** — use the explicit pipeline pattern: Source → Mapper → Actor → Renderer → Window → Interactor. Do not use convenience methods or shortcut wrappers.
- **No `vtkNamedColors`** — define colors as normalized RGB tuples with descriptive names (e.g. `midnight_blue_rgb = (0.098, 0.098, 0.439)`).
- **Factory overrides** — always import the factory registration modules at the top:
  ```python
  import vtkmodules.vtkInteractionStyle  # noqa: F401
  import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
  ```
- **Explicit imports** — import each VTK class individually from its `vtkmodules` subpackage. Do not use `import vtk`.
- **Variable naming** — use `snake_case` for all variables. Name variables after what they represent, not the VTK class (e.g. `poly_data_mapper` not `mapper`, `arrow_source` not `source`).
- **Comments** — annotate each pipeline stage (Source, Mapper, Actor, Renderer, Window, Interactor) with a short comment.
- **Window name** — set `render_window.SetWindowName("Title")` to match the example title.
- **End with interactor** — every example ends with `Initialize()` and `Start()`.

## Chart examples (Plotting category)

Chart examples use `vtkContextActor` to overlay 2D charts on the rendering pipeline. The pattern is:

**Data (vtkTable) → Chart (vtkChartXY) → ContextActor → Renderer → Window → Interactor**

- Import `vtkmodules.vtkRenderingContextOpenGL2` in addition to the standard factory overrides.
- Create a `vtkTable` with `vtkFloatArray`/`vtkIntArray` columns for the data.
- Create a chart (`vtkChartXY`, `vtkChartPie`, etc.) and add plot series.
- Wrap the chart in a `vtkContextActor` and add it to the renderer via `renderer.AddActor(context_actor)`.
- Call `context_actor.GetScene().SetRenderer(renderer)` to connect the scene.
- Set `render_window.SetMultiSamples(0)` to avoid aliasing artifacts with 2D rendering.

See `Plotting/BarChart.py` for a reference implementation.

## Graph examples (Graphs category)

Graph examples use `vtkGraphLayoutView`, which manages its own renderer, window, and interactor internally. The pattern is:

**Graph (vtkMutableUndirectedGraph) → View (vtkGraphLayoutView)**

- Build the graph by adding vertices and edges.
- Create a `vtkGraphLayoutView`, call `AddRepresentationFromInput(graph)`, and set a layout strategy.
- Access the render window via `view.GetRenderWindow()` and the interactor via `view.GetInteractor()`.
- Set background colors on `view.GetRenderer()`.

See `Graphs/ConstructGraph.py` for a reference implementation.

## Markdown file standards

The companion `.md` file follows this format (see `Arrow.md`):

```markdown
### Description

One or two sentences describing what the example demonstrates.

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkClassName](https://www.vtk.org/doc/nightly/html/classvtkClassName.html) — what it does in this example.
- Repeat for each VTK class used, in alphabetical order.
```

- Start with `### Description` (h3, not h1/h2 — the site generator handles the page title).
- Include the pipeline summary in bold on its own line.
- List every VTK class used with a link to its Doxygen page and a brief explanation of its role.
- List classes in **alphabetical order**.

## Submitting a new example

### 1. Fork and clone the repository

Fork [Kitware/vtk-python-examples](https://github.com/Kitware/vtk-python-examples) on GitHub, then clone your fork:

```bash
git clone https://github.com/<your-username>/vtk-python-examples.git
cd vtk-python-examples
```

### 2. Set up the development environment

`uv sync` creates a `.venv` in the project directory automatically if one doesn't exist.

```bash
uv sync                                        # creates .venv and installs all dependencies
cd docs && npm install && cd ..                 # installs VitePress for the docs site
uv run python scripts/generate_examples_jsonl.py  # generates all doc pages and assets
cd docs && npx vitepress dev                    # starts the local website at http://localhost:5173/vtk-python-examples/
```

To include PyQt6 for the Qt examples:

```bash
uv sync --extra qt
```

### 3. Create a branch

```bash
git checkout -b add-example-{Category}-{Title}
```

### 4. Create the example files

- `src/Python/{Category}/{Title}.py` — following the Python file standards above
- `src/Python/{Category}/{Title}.md` — following the markdown file standards above
- If the example requires data files, place them alongside the `.py` file

### 5. Add a manifest entry

Add an entry to `src/tests/test_manifest.json`:

```json
{
    "category": "Category",
    "title": "Title",
    "script_path": "src/Python/Category/Title.py",
    "output_image": "Category_Title.png",
    "render_window_var": "render_window"
}
```

### 6. Run the test to generate a screenshot

```bash
uv run python src/tests/test_examples.py --example {Category}/{Title}
```

Verify the screenshot was saved to `data/images/testing/Category_Title.png`.

### 7. Rebuild the docs and preview

```bash
uv run python scripts/generate_examples_jsonl.py
cd docs && npx vitepress dev
```

Browse to `http://localhost:5173/vtk-python-examples/examples/{Category}/{Title}` and verify the example page looks correct.

### 8. Commit and submit a pull request

```bash
git add -A
git commit -m "Add {Category}/{Title} example"
git push origin add-example-{Category}-{Title}
```

Open a pull request from your fork to [Kitware/vtk-python-examples](https://github.com/Kitware/vtk-python-examples) on GitHub.
