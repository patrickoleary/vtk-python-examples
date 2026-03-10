### Description

This example removes statistical outlier points from a point cloud using vtkStatisticalOutlierRemoval. Points whose mean distance to neighbors deviates significantly from the cloud average are removed. The left viewport shows the original cloud with scattered outliers and the right shows the cleaned result. It follows the VTK pipeline structure:

**PointCloud → StatisticalOutlierRemoval → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the original and cleaned clouds.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- [vtkStatisticalOutlierRemoval](https://www.vtk.org/doc/nightly/html/classvtkStatisticalOutlierRemoval.html) computes the mean distance from each point to its k nearest neighbors and removes points that are more than a specified number of standard deviations from the mean. `SetSampleSize(20)` sets the neighbor count and `SetStandardDeviationFactor(1.5)` controls the threshold.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
