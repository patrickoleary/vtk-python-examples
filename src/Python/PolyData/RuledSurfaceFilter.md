### Description

This example generates a ruled surface between two line segments using vtkRuledSurfaceFilter.

**Lines → RuledSurfaceFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores the line cell connectivity.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) defines individual line segments.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the endpoints of the two line segments.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the line geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface to graphics primitives.
- [vtkRuledSurfaceFilter](https://www.vtk.org/doc/nightly/html/classvtkRuledSurfaceFilter.html) generates the ruled surface between the two lines.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
