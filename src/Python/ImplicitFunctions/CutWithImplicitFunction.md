### Description

This example cuts a tessellated sphere with an implicit plane using vtkCutter to extract the cross-section contour. The contour line is drawn as a thick red ring at the equator, while the full sphere is shown as a translucent wireframe for context. It follows the VTK pipeline structure:

**SphereSource → Cutter (with vtkPlane) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors are used: a thick red contour line and a translucent grey wireframe sphere for context.
- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) extracts the intersection contour where the plane meets the sphere surface. Unlike clipping (which removes geometry), cutting produces only the intersection line.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit cut function — a plane through the origin with normal along Z, slicing the sphere at its equator.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps both the contour line and the sphere wireframe to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere with 40×40 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
