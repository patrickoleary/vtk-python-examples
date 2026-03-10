### Description

This example densifies a sparse point cloud using vtkDensifyPointCloudFilter. The left viewport shows the original sparse cloud on a hemisphere and the right shows the densified result with additional interpolated points. It follows the VTK pipeline structure:

**PointCloud → DensifyPointCloudFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the sparse and densified clouds.
- [vtkDensifyPointCloudFilter](https://www.vtk.org/doc/nightly/html/classvtkDensifyPointCloudFilter.html) adds points to a point cloud so that the distance between neighboring points does not exceed a target distance. `SetTargetDistance(0.1)` controls the maximum spacing and `SetMaximumNumberOfIterations(3)` limits the densification passes.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
