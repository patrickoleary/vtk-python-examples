### Description

This example reads GPS track points from a CSV file, builds a colored point cloud, writes selected columns back to a new CSV file using Python's `csv` module, and renders the result.

**Reader → PolyData Construction → CSV Writer → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetPointSize()` increases the point size for visibility.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkDelimitedTextReader](https://www.vtk.org/doc/nightly/html/classvtkDelimitedTextReader.html) is used a second time to read the written CSV back, verifying the round-trip.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) holds elevation values as point scalars for coloring.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the easting, northing, and elevation coordinates as 3D points extracted from the table columns.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) assembles the points and vertex cells into a renderable point cloud dataset.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the point cloud to graphics primitives with scalar coloring enabled.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
