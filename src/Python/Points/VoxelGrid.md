### Description

This example downsamples a point cloud using vtkVoxelGrid. The left viewport shows the original dense spherical cloud colored by elevation and the right shows the voxelized result with one representative point per voxel. It follows the VTK pipeline structure:

**PointCloud → VoxelGrid → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the dense and downsampled clouds.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- [vtkVoxelGrid](https://www.vtk.org/doc/nightly/html/classvtkVoxelGrid.html) downsamples a point cloud by binning points into voxels and replacing each bin with a single representative point. `SetConfigurationStyleToLeafSize()` and `SetLeafSize(0.15, 0.15, 0.15)` control the voxel dimensions.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
