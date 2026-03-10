### Description

This example clips a tessellated sphere with an implicit plane using vtkClipPolyData. The retained half is shown in peach puff and the clipped-away half is shown as a translucent tomato red ghost, making the clip operation clearly visible. It follows the VTK pipeline structure:

**SphereSource → ClipPolyData (with vtkPlane) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors are used: the retained half in peach puff and the clipped half in translucent tomato red.
- [vtkClipPolyData](https://www.vtk.org/doc/nightly/html/classvtkClipPolyData.html) removes all geometry on the positive side of the plane. `SetClipFunction()` specifies the implicit function. `GenerateClippedOutputOn()` keeps the removed portion available via `GetClippedOutputPort()`.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit clip function — a plane through the origin with normal along X.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps both the retained and clipped surfaces to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere with 30×30 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
