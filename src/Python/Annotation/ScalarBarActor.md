### Description

This example demonstrates a standalone scalar bar annotation showing a color lookup table mapped to elevation on a sphere. The scalar bar displays the color legend alongside the visualization.

**Source → Elevation Filter → Lookup Table → Mapper → Actor → Scalar Bar → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Scalar coloring from the elevation filter drives the surface appearance.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) computes scalar values based on distance along a specified direction (Z axis). `SetLowPoint()` and `SetHighPoint()` define the scalar range endpoints.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors. `SetHueRange(0.667, 0.0)` creates a blue-to-red ramp.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives with scalar coloring enabled.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays a color legend mapping scalar values to colors. `SetTitle()` labels the bar, `SetNumberOfLabels()` controls tick marks, and `SetOrientationToVertical()` sets the layout direction. `SetPosition()`, `SetWidth()`, and `SetHeight()` control placement and size.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere polygon mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
