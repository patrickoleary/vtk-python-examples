### Description

This example smooths a noisy sphere using vtkWindowedSincPolyDataFilter, which applies a windowed sinc function as a low-pass filter on the mesh geometry. Unlike Laplacian smoothing, windowed sinc smoothing better preserves sharp features while removing high-frequency noise. Side-by-side viewports show before (left) and after (right). It follows the VTK pipeline structure:

**SphereSource → Random Perturbation → WindowedSincPolyDataFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors in peach-puff color, one per viewport.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized navigation.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) adds reproducible random noise to each vertex position.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the noisy and smoothed meshes to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere with 30×30 resolution.
- [vtkWindowedSincPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkWindowedSincPolyDataFilter.html) applies 20 iterations of windowed sinc smoothing with a pass band of 0.1. `NormalizeCoordinatesOn()` scales coordinates to [−1, 1] before filtering for numerical stability.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
