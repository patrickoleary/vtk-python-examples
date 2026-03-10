### Description

This example smooths a noisy point cloud using vtkPointInterpolator with a vtkGaussianKernel. The left viewport shows the noisy input colored by a scalar field and the right shows the smoothed result. It follows the VTK pipeline structure:

**PointCloud → PointInterpolator (with GaussianKernel) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the noisy and smoothed clouds.
- [vtkGaussianKernel](https://www.vtk.org/doc/nightly/html/classvtkGaussianKernel.html) defines a Gaussian interpolation kernel. `SetSharpness(2.0)` controls the falloff rate and `SetRadius(0.5)` sets the support radius.
- [vtkPointInterpolator](https://www.vtk.org/doc/nightly/html/classvtkPointInterpolator.html) interpolates point data from a source point cloud onto the input points using the specified kernel. This effectively smooths the scalar field.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
