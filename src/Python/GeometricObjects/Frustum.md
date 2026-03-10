### Description

This example extracts the frustum planes from a vtkCamera and displays the frustum geometry with shrunk faces, edge visibility, and backface coloring. It follows the standard VTK pipeline structure:

**Camera → Planes → Source → Filter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the frustum with `EdgeVisibilityOn()` and a backface property via [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html).
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the view frustum via `SetClippingRange()`. `GetFrustumPlanes()` extracts the six clipping planes.
- [vtkFrustumSource](https://www.vtk.org/doc/nightly/html/classvtkFrustumSource.html) generates the frustum geometry from the planes.
- [vtkPlanes](https://www.vtk.org/doc/nightly/html/classvtkPlanes.html) stores the frustum planes via `SetFrustumPlanes()`.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the geometry to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkShrinkPolyData](https://www.vtk.org/doc/nightly/html/classvtkShrinkPolyData.html) shrinks each face slightly to reveal edges via `SetShrinkFactor()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a silver background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
