### Description

This example visualizes an implicit cone by sampling it on a volume grid using vtkSampleFunction and extracting the zero isosurface with vtkContourFilter. The cone has a 30-degree half-angle along the X axis, producing a double-cone (hourglass) shape clipped by the sampling bounds and rendered in tomato red. It follows the VTK pipeline structure:

**Cone → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with tomato red color.
- [vtkCone](https://www.vtk.org/doc/nightly/html/classvtkCone.html) defines an implicit cone function. `SetAngle(30.0)` sets the half-angle in degrees. The cone axis is along X by default and the apex is at the origin, producing a double-cone (both sides of the apex).
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface — the conical surface clipped by the sampling bounds.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit cone on a regular 60×60×60 grid over [−1.5, 1.5]³.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
