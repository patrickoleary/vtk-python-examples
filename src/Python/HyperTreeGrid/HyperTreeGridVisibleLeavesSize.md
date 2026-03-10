### Description

This example computes visible leaf cell sizes in a hyper tree grid using vtkHyperTreeGridGenerateFields and colors the surface by the computed cell-size array. Small refined cells appear blue and large coarse cells appear red using a diverging color transfer function. It follows the VTK pipeline structure:

**Source → VisibleLeavesSize → Geometry → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with `EdgeVisibilityOn()` to show cell boundaries.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) maps the cell-size scalar range to a blue-white-red diverging colormap.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of the HTG as polydata for rendering.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field.
- [vtkHyperTreeGridGenerateFields](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGenerateFields.html) computes derived cell data arrays for a hyper tree grid. `SetComputeCellSizeArray(True)` enables computation of cell sizes (volumes) for each visible leaf. This replaces the deprecated vtkHyperTreeGridVisibleLeavesSize.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface polydata to graphics primitives. `SetScalarModeToUseCellFieldData()` and `SelectColorArray()` color by the computed size array.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
