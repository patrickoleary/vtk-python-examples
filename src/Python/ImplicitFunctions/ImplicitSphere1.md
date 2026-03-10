### Description

This example visualizes an implicit sphere with visible mesh edges by sampling it on a volume grid using vtkSampleFunction and extracting the zero isosurface with vtkContourFilter. The sphere has radius 0.5 and is rendered in alice blue with steel blue edges, showing the triangulation of the isosurface. It follows the VTK pipeline structure:

**Sphere → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry with `EdgeVisibilityOn()` to show the mesh wireframe.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit sphere on a regular 20×20×20 grid over [−0.5, 0.5]³. The coarser grid makes the mesh triangulation clearly visible.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) defines an implicit sphere function with `SetRadius(0.5)`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
