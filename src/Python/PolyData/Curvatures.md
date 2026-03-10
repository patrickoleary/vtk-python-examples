### Description

This example computes Mean curvature on a cowHead mesh, adjust edge curvatures via distance-weighted averaging of interior neighbours, and display the result with a colour-mapped scalar bar.

**Reader → Curvatures → EdgeAdjustment → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCameraOrientationWidget](https://www.vtk.org/doc/nightly/html/classvtkCameraOrientationWidget.html) provides an interactive orientation gizmo.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) provides a predefined set of colours used to build the lookup table.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) maps scalar curvature values to colours.
- [vtkCurvatures](https://www.vtk.org/doc/nightly/html/classvtkCurvatures.html) computes Mean curvature at each vertex.
- [vtkFeatureEdges](https://www.vtk.org/doc/nightly/html/classvtkFeatureEdges.html) extracts boundary edges to identify points needing curvature adjustment.
- [vtkGenerateIds](https://www.vtk.org/doc/nightly/html/classvtkGenerateIds.html) assigns original point IDs so boundary points can be mapped back after edge extraction.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) stores neighbour point IDs during edge curvature adjustment.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the curvature-coloured mesh to graphics primitives.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the curvature legend.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) loads `cowHead.vtp` from the data directory.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
