### Description

This example removes outlier points from a point cloud using vtkRadiusOutlierRemoval. Points that do not have enough neighbors within a specified radius are removed. The left viewport shows the original cloud with scattered outliers and the right shows the cleaned result. It follows the VTK pipeline structure:

**PointCloud → RadiusOutlierRemoval → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the original and cleaned clouds.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRadiusOutlierRemoval](https://www.vtk.org/doc/nightly/html/classvtkRadiusOutlierRemoval.html) removes points that have fewer than a minimum number of neighbors within a given radius. `SetRadius(0.3)` defines the search radius and `SetNumberOfNeighbors(5)` sets the minimum neighbor count.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
