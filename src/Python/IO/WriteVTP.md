### Description

This example reads GPS track points from a CSV file, builds a colored polyline, writes it to a VTP file, reads it back, and renders the result.

**Reader → PolyData Construction → VTP Writer → VTP Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkDelimitedTextReader](https://www.vtk.org/doc/nightly/html/classvtkDelimitedTextReader.html) reads the CSV file into a `vtkTable`. `DetectNumericColumnsOn()` automatically parses numeric fields.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the easting, northing, and elevation coordinates as 3D points extracted from the table columns.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) assembles the points, elevation scalars, and line cells into a dataset.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives with scalar coloring enabled.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) reads the written VTP file back, verifying the round-trip.
- [vtkXMLPolyDataWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataWriter.html) writes the polydata to a VTP file. `SetFileName()` specifies the output path.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
