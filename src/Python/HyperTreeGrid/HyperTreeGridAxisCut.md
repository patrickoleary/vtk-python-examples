### Description

This example cuts a hyper tree grid with an axis-aligned plane using vtkHyperTreeGridAxisCut. The filter produces a 2D slice through the 3D HTG at a specified position along the Y axis. The slice is rendered colored by Depth with the full HTG wireframe shown as translucent context. It follows the VTK pipeline structure:

**Source → AxisCut → Geometry → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the cut slice and the context wireframe.
- [vtkHyperTreeGridAxisCut](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridAxisCut.html) extracts a 2D slice from a hyper tree grid along an axis-aligned plane. `SetPlaneNormalAxis(1)` selects the Y axis and `SetPlanePosition(1.5)` sets the cut location. The output is a lower-dimensional HTG.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of the HTG as polydata for rendering.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
