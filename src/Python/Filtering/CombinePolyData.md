### Description

This example combines a sphere and a cone into a single polydata using vtkAppendPolyData, removes duplicate points with vtkCleanPolyData, and displays the merged result.

**Sphere + Cone → AppendPolyData → CleanPolyData → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAppendPolyData](https://www.vtk.org/doc/nightly/html/classvtkAppendPolyData.html) merges multiple polydata inputs into one.
- [vtkCleanPolyData](https://www.vtk.org/doc/nightly/html/classvtkCleanPolyData.html) removes duplicate points from the combined mesh.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone at the origin.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cleaned polydata to graphics primitives. Connected to the clean filter via `SetInputConnection()`.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere offset along the X axis.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. `GetActiveCamera().Zoom()` adjusts the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
