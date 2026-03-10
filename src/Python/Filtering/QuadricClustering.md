### Description

This example demonstrates vtkQuadricClustering for mesh simplification. A high-resolution sphere is decimated and shown side-by-side with the original.

**SphereSource → QuadricClustering → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` shows the mesh edges.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the original and decimated meshes to graphics primitives.
- [vtkQuadricClustering](https://www.vtk.org/doc/nightly/html/classvtkQuadricClustering.html) simplifies a mesh by clustering vertices within spatial bins and collapsing each bin using quadric error metrics.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the high-resolution sphere.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. Two viewports show the comparison.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
