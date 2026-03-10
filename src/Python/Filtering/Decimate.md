### Description

This example reduces the polygon count of a sphere by 80% using vtkDecimatePro and displays the original and decimated meshes side by side with visible edges to show the difference in triangle density.

**SphereSource → Original Mapper + DecimatePro → Decimated Mapper → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` reveals individual triangles; `SetPosition()` offsets the two meshes for side-by-side comparison.
- [vtkDecimatePro](https://www.vtk.org/doc/nightly/html/classvtkDecimatePro.html) performs mesh simplification by reducing the number of triangles while preserving topology. `SetTargetReduction(0.8)` removes approximately 80% of the triangles.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the original and decimated meshes to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a high-resolution sphere (40x40) providing enough triangles for meaningful decimation.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. `ResetCamera()` frames both meshes.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
