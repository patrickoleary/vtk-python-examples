### Description

This example computes point density on a regular grid using vtkPointDensityFilter. A procedural 2D point cloud with two overlapping clusters is projected onto a density image and rendered alongside the semi-transparent point cloud. It follows the VTK pipeline structure:

**PointCloud → PointDensityFilter → ImageActor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. The point cloud is rendered semi-transparently over the density image.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the density image as a 2D slice.
- [vtkPointDensityFilter](https://www.vtk.org/doc/nightly/html/classvtkPointDensityFilter.html) computes a scalar density field on a regular grid from a point cloud. `SetDensityEstimateToFixedRadius()` uses a fixed-radius kernel, `SetRadius(0.3)` sets the kernel radius, and `SetSampleDimensions()` controls the output resolution.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the point cloud polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
