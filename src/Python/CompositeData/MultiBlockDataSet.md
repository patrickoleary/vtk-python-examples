### Description

This example builds a nested vtkMultiBlockDataSet tree with three sphere sources, extracts edges from all blocks using a non-composite-aware filter, and renders the wireframe using a composite geometry filter that aggregates the output into one polydata.

**Sources → Nested Multi-Block → Extract Edges → Composite Geometry → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the wireframe color to gold. `GetProperty().SetLineWidth()` thickens the edge lines.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) aggregates all composite blocks into a single polydata for rendering.
- [vtkExtractEdges](https://www.vtk.org/doc/nightly/html/classvtkExtractEdges.html) extracts the edges of each block. As a non-composite-aware filter, the pipeline automatically iterates over all blocks.
- [vtkMultiBlockDataSet](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockDataSet.html) assembles datasets into a hierarchical tree. A branch multiblock is nested inside the root multiblock, demonstrating multi-level nesting.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the aggregated edge polydata to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere polygon meshes at different positions and sizes.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
