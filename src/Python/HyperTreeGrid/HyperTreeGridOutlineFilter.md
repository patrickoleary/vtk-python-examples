### Description

This example displays the bounding box outline of a hyper tree grid alongside its semi-transparent surface colored by the Depth scalar. The outline provides a spatial reference frame for the adaptive mesh. It follows the VTK pipeline structure:

**Source → Geometry → OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors are used — the HTG surface colored by Depth with `SetOpacity(0.5)` and `EdgeVisibilityOn()`, and the bounding box outline in white with `SetLineWidth(3)`.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of the HTG as polydata.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field. `SetActiveScalars("Depth")` is called so downstream filters can find the scalar data.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) computes the axis-aligned bounding box of the geometry as a wireframe cube.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface and outline polydata to graphics primitives. `SetScalarModeToUseCellFieldData()` and `SelectColorArray("Depth")` color the surface by the Depth scalar.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
