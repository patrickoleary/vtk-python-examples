### Description

This example demonstrates two ways to create [vtkPlanes](https://www.vtk.org/doc/nightly/html/classvtkPlanes.html): from camera frustum planes and from bounding-box bounds. A solid sphere is placed inside the frustum, and its bounding-box hull is shown as a wireframe around it — all in the same coordinate space. It follows the VTK pipeline structure:

**Source → Filter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) renders the sphere as a solid light blue surface, the frustum hull as a moccasin wireframe, and the bounding-box hull as a light coral wireframe.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) provides frustum planes via `GetFrustumPlanes()` with a custom clipping range.
- [vtkHull](https://www.vtk.org/doc/nightly/html/classvtkHull.html) generates a convex hull polyhedron from each set of planes via `GenerateHull()`.
- [vtkPlanes](https://www.vtk.org/doc/nightly/html/classvtkPlanes.html) stores each set of planes — created by `SetFrustumPlanes()` for the frustum and `SetBounds()` for the sphere's bounding box.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the sphere surface and each hull to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere positioned within the frustum volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark slate gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
