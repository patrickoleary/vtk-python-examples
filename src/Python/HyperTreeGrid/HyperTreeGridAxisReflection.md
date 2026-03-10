### Description

This example mirrors a hyper tree grid across the X axis using vtkHyperTreeGridAxisReflection and renders both the original and reflected copies together in a single scene, colored by the Depth scalar. It follows the VTK pipeline structure:

**Source → AxisReflection → Geometry → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors are used — the original and the reflected copy, both colored by Depth with `EdgeVisibilityOn()` to show cell boundaries.
- [vtkHyperTreeGridAxisReflection](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridAxisReflection.html) mirrors the hyper tree grid across an axis-aligned plane. `SetPlaneToXMin()` reflects across the plane at the minimum X coordinate. Other options include `SetPlaneToXMax()`, `SetPlaneToYMin()`, `SetPlaneToYMax()`, `SetPlaneToZMin()`, and `SetPlaneToZMax()`.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of each HTG as polydata.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field. `SetActiveScalars("Depth")` is called so downstream filters can find the scalar data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface polydata to graphics primitives. `SetScalarModeToUseCellFieldData()` and `SelectColorArray("Depth")` color both surfaces by the Depth scalar.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
