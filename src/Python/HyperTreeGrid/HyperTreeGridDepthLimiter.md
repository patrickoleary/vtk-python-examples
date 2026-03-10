### Description

This example coarsens a hyper tree grid by capping the tree depth at level 2 using vtkHyperTreeGridDepthLimiter, then renders the coarsened surface colored by the Depth scalar. It follows the VTK pipeline structure:

**Source → DepthLimiter → Geometry → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry with `EdgeVisibilityOn()` to show cell boundaries.
- [vtkHyperTreeGridDepthLimiter](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridDepthLimiter.html) coarsens the hyper tree grid by removing all nodes deeper than the specified level. `SetDepth(2)` caps the tree at depth 2, collapsing fine detail into coarse cells. This is useful for previewing large datasets at reduced resolution.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of the depth-limited HTG as polydata.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with up to 6 levels of refinement. A `Depth` cell scalar is generated automatically.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface polydata to graphics primitives. `SetScalarRange()` maps the Depth scalar to the default color lookup table.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
