### Description

This example visualizes an implicit plane by sampling it on a volume grid using vtkSampleFunction and extracting the zero isosurface with vtkContourFilter. The plane passes through the origin with normal (1, 1, 1), producing a flat diagonal surface rendered in tomato red with black edges. It follows the VTK pipeline structure:

**Plane → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with tomato red color and black edges.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface from the sampled volume — the set of points where the distance is zero, which is the plane itself.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines an implicit plane function. `SetOrigin()` places the plane through the origin and `SetNormal(1, 1, 1)` tilts it diagonally. The implicit function evaluates to the signed distance from the plane at any point.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit plane on a regular 50×50×50 grid over the domain [−2, 2]³, producing a scalar volume where each voxel stores its signed distance from the plane.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
