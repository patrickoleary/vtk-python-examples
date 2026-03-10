### Description

This example generates a noisy sphere by perturbing point positions with random offsets, then smooths it with vtkSmoothPolyDataFilter using 50 Laplacian iterations. The noisy and smoothed meshes are displayed side by side.

**SphereSource → Perturb Points → Noisy Mapper + SmoothPolyDataFilter → Smooth Mapper → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` reveals individual triangles; `SetPosition()` offsets the two meshes for side-by-side comparison.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) adds deterministic random noise to the sphere vertices.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the noisy and smoothed meshes to graphics primitives.
- [vtkSmoothPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkSmoothPolyDataFilter.html) performs Laplacian smoothing, iteratively averaging each point's position with its neighbors to reduce noise while preserving overall shape.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. `ResetCamera()` frames both meshes.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
