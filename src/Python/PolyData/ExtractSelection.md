### Description

This example extracts a subset of points by index using vtkExtractSelection, showing all points, selected points, and non-selected points in three viewports.

**Source → Selection → ExtractSelection → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) provides a shared camera across the three viewports.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the point sets to graphics primitives.
- [vtkExtractSelection](https://www.vtk.org/doc/nightly/html/classvtkExtractSelection.html) extracts the selected points and (with inverse flag) the unselected remainder.
- [vtkIdTypeArray](https://www.vtk.org/doc/nightly/html/classvtkIdTypeArray.html) stores the point IDs to be selected.
- [vtkPointSource](https://www.vtk.org/doc/nightly/html/classvtkPointSource.html) generates a random point cloud.
- [vtkSelection](https://www.vtk.org/doc/nightly/html/classvtkSelection.html) wraps the selection node into a selection object.
- [vtkSelectionNode](https://www.vtk.org/doc/nightly/html/classvtkSelectionNode.html) specifies which points to extract by their IDs.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the extracted point subsets.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
