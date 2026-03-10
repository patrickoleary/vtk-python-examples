### Description

This example smooths a noisy sphere using vtkSmoothPolyDataFilter, which applies iterative Laplacian smoothing to reduce surface noise. A sphere is perturbed with random noise to create a bumpy surface, then smoothed over 200 iterations. Side-by-side viewports show the noisy input (left) and the smoothed result (right). It follows the VTK pipeline structure:

**SphereSource → Random Perturbation → SmoothPolyDataFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors in peach-puff color, one per viewport.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized navigation.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) adds reproducible random noise to each vertex position to create a bumpy surface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the noisy and smoothed meshes to graphics primitives.
- [vtkSmoothPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkSmoothPolyDataFilter.html) applies 200 iterations of Laplacian smoothing with a relaxation factor of 0.1. Each iteration moves vertices toward the average of their neighbors.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere with 30×30 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
