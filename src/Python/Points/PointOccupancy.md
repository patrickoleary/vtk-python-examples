### Description

This example computes point occupancy on a regular grid using vtkPointOccupancyFilter. A procedural spiral point cloud is binned into voxels and the occupancy count is rendered as an image slice overlaid with the semi-transparent point cloud. It follows the VTK pipeline structure:

**PointCloud → PointOccupancyFilter → ImageActor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. The point cloud is rendered semi-transparently over the occupancy image.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the occupancy grid as a 2D image.
- [vtkPointOccupancyFilter](https://www.vtk.org/doc/nightly/html/classvtkPointOccupancyFilter.html) bins points into a regular grid and sets each voxel to an occupied or empty value. `SetSampleDimensions()` controls the grid resolution, `SetOccupiedValue(255)` and `SetEmptyValue(0)` define the output range.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the point cloud polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
