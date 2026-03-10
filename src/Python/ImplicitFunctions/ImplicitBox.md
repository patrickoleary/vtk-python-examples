### Description

This example visualizes an implicit box by sampling it on a volume grid using vtkSampleFunction and extracting the zero isosurface with vtkContourFilter. The box is axis-aligned with non-uniform dimensions (wider along Y), rendered in alice blue with steel blue edges showing the mesh triangulation. It follows the VTK pipeline structure:

**Box → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry with `EdgeVisibilityOn()` to show the mesh wireframe.
- [vtkBox](https://www.vtk.org/doc/nightly/html/classvtkBox.html) defines an implicit box function via `SetBounds()`. The implicit function evaluates to the signed distance from the box boundary — negative inside, positive outside.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface — the box surface with rounded edges from the marching cubes algorithm.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit box on a regular 50×50×50 grid over [−1.5, 1.5]³.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
