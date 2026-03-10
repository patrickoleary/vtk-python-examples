### Description

This example visualizes an implicit sphere by sampling it on a volume grid using vtkSampleFunction and extracting the zero isosurface with vtkContourFilter. The sphere is centered at the origin with radius 1, rendered in tomato red. It follows the VTK pipeline structure:

**Sphere → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with tomato red color.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface — the set of points where the implicit function is zero, which is the sphere surface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit sphere on a regular 50×50×50 grid over the domain [−2, 2]³, producing a scalar volume.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) defines an implicit sphere function. `SetCenter()` places the sphere at the origin and `SetRadius(1.0)` sets the unit radius. The implicit function evaluates to `x² + y² + z² - r²` at any point.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
