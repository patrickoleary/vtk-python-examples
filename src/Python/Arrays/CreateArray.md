### Description

This example creates a custom scalar array based on the radial distance from the Z axis, attaches it to a sphere's point data, and visualizes the result with a color lookup table and scalar bar.

**Source → Custom Array → Lookup Table → Mapper → Actor → Scalar Bar → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Scalar coloring from the distance array drives the surface appearance.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) creates a custom scalar array. `SetName()` assigns a name to the array. `SetNumberOfTuples()` pre-allocates storage. `SetValue()` populates each element with the computed distance.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors. `SetHueRange(0.667, 0.0)` creates a blue-to-red color ramp.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives with scalar coloring enabled.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays a color legend alongside the visualization.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere polygon mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
