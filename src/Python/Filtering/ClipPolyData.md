### Description

This example clips a sphere with a plane using vtkClipPolyData and displays both the kept half and the clipped-away half side by side with visible edges.

**SphereSource → ClipPolyData (with Plane) → Kept Mapper + Clipped Mapper → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` shows the mesh edges; `SetPosition()` offsets the clipped half along X.
- [vtkClipPolyData](https://www.vtk.org/doc/nightly/html/classvtkClipPolyData.html) splits the sphere into two halves based on the implicit function sign. `GenerateClippedOutputOn()` retains both the negative-side (kept) and positive-side (clipped) outputs.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit clipping function — a plane through the origin with an X-axis normal.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the kept and clipped halves to graphics primitives. Connected via `GetOutputPort()` and `GetClippedOutputPort()`.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. `ResetCamera()` frames both halves.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
