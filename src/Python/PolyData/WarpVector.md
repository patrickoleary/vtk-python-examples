### Description

This example displaces a polyline by per-point vectors using vtkWarpVector.

**Points → Lines → WarpVector → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores the line cell connectivity.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores the displacement vectors for each point.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) defines individual line segments.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the polyline vertex positions.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the polyline geometry and vector data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the original and warped polylines to graphics primitives.
- [vtkWarpVector](https://www.vtk.org/doc/nightly/html/classvtkWarpVector.html) displaces the polyline points by their associated vectors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
