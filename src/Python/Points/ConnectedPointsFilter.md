### Description

This example extracts connected point regions from a point cloud using vtkConnectedPointsFilter. Three separated clusters of points are created procedurally and the filter groups them by proximity, coloring each region distinctly. It follows the VTK pipeline structure:

**PointCloud → ConnectedPointsFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with `SetPointSize(5)` for visibility.
- [vtkConnectedPointsFilter](https://www.vtk.org/doc/nightly/html/classvtkConnectedPointsFilter.html) groups points into connected regions based on proximity. `SetRadius(0.5)` defines the neighborhood distance, `SetExtractionModeToAllRegions()` extracts all regions, and `SetColorRegions(True)` assigns a region ID scalar to each point.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
