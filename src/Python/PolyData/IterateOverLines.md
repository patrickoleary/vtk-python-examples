### Description

This example builds a polydata with line cells, iterate over them printing connectivity, and render.

**Points → Lines → PolyData → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) creates two polyline cells connecting subsets of points.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) retrieves point IDs for each line cell during iteration.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) defines individual line segments within the polylines.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the five points used by the polylines.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) stores the polyline geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polylines to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
