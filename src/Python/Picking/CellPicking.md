### Description

This example cells picking on a triangulated plane. Left-click on the plane to pick a cell; the selected cell is highlighted in red with visible edges. The picked cell ID and world-space coordinates are printed to the console. A custom interactor style subclasses vtkInteractorStyleTrackballCamera to override left-button press handling.

**vtkPlaneSource → vtkTriangleFilter → vtkPolyDataMapper → Actor + vtkCellPicker → vtkExtractSelection → highlight actor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellPicker](https://www.vtk.org/doc/nightly/html/classvtkCellPicker.html) performs cell-level picking at the click position.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the extracted selection for rendering.
- [vtkExtractSelection](https://www.vtk.org/doc/nightly/html/classvtkExtractSelection.html) extracts the picked cell into a separate dataset.
- [vtkIdTypeArray](https://www.vtk.org/doc/nightly/html/classvtkIdTypeArray.html) provides id type array functionality.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) base class for the custom interactor.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates a planar quad.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSelection](https://www.vtk.org/doc/nightly/html/classvtkSelection.html) provides selection functionality.
- [vtkSelectionNode](https://www.vtk.org/doc/nightly/html/classvtkSelectionNode.html) specifies the selection by cell index.
- [vtkTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkTriangleFilter.html) triangulates the plane for cell picking.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) represents unstructured geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
