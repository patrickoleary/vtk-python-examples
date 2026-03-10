### Description

This example smooths a point cloud using vtkPointSmoothingFilter. The left viewport shows the original noisy spherical point cloud colored by elevation and the right shows the smoothed result where points have been relaxed toward local centroids. It follows the VTK pipeline structure:

**PointCloud → PointSmoothingFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the noisy and smoothed clouds.
- [vtkPointSmoothingFilter](https://www.vtk.org/doc/nightly/html/classvtkPointSmoothingFilter.html) relaxes point positions toward local neighborhood centroids. `SetNumberOfIterations(20)` controls the smoothing passes and `SetNeighborhoodSize(16)` sets how many neighbors influence each point.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
