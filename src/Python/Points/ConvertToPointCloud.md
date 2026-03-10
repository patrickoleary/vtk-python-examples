### Description

This example converts polydata vertices to a point cloud using vtkConvertToPointCloud. The left viewport shows the original sphere mesh with edges and the right shows the resulting point cloud. It follows the VTK pipeline structure:

**SphereSource → ConvertToPointCloud → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the mesh and the point cloud.
- [vtkConvertToPointCloud](https://www.vtk.org/doc/nightly/html/classvtkConvertToPointCloud.html) strips all cells from a polydata dataset and outputs only the points as a vertex-only point cloud.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere with 30×30 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
