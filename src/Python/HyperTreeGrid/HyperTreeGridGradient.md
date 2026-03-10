### Description

This example computes the gradient of a scalar field on a hyper tree grid using vtkHyperTreeGridGradient and displays the result in a side-by-side layout. The left viewport shows the HTG surface colored by the Depth scalar (red for coarse cells, progressing through yellow, green, and cyan for increasingly refined cells). The right viewport shows the same surface in greyscale colored by gradient magnitude — coarse cells (depth ≤ 1) are forced to black so they do not dominate the image. Refined cells near refinement boundaries appear as bright grey-to-white blocks, while refined cells in uniform interior regions stay dark. The result highlights exactly where resolution transitions occur in the grid. A log-scale lookup table spreads the greyscale values to show more variation. It follows the VTK pipeline structure:

**Source → Geometry → Mapper → Actor (left, Depth coloring)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` draws black edges to show cell boundaries.
- [vtkArrayCalculator](https://www.vtk.org/doc/nightly/html/classvtkArrayCalculator.html) computes `GradientMagnitude = mag(Gradient)` for cells with depth > 1, zeroing out coarse cells so they stay dark and only refined regions show gradient variation.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of the HTG.
- [vtkHyperTreeGridGradient](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGradient.html) computes the gradient of the Depth scalar field. `SetInputArrayToProcess()` specifies which array to differentiate. The output contains both the original `Depth` scalar and a new `Gradient` vector array.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface to graphics primitives. The left mapper colors by `Depth`; the right mapper colors by `GradientMagnitude`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
