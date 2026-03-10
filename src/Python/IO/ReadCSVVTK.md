### Description

This example reads ECEF coordinates from a CSV file using `vtkDelimitedTextReader` and overlays two versions of the track in a single renderer: the original (centroid-translated, black) and a rotated version (diverging color map by elevation). The centroid translation brings the data to the origin so the ECEF-to-local rotation is clearly visible.

**CSV → vtkDelimitedTextReader → vtkTableToPolyData → Transforms → Mappers → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors are used — the original track in solid black via `GetProperty().SetColor()` and the rotated track colored by elevation. Both use `SetLineWidth(2)`.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines a diverging color map (cool blue → white → warm red) using `SetColorSpaceToDiverging()` and three RGB control points.
- [vtkDelimitedTextReader](https://www.vtk.org/doc/nightly/html/classvtkDelimitedTextReader.html) reads the CSV file directly into a `vtkTable`. `DetectNumericColumnsOn()` automatically parses numeric fields; `SetFieldDelimiterCharacters(",")` and `SetHaveHeaders(True)` configure the CSV format.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) is populated from the color transfer function to map elevation values to colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each version to graphics primitives. The original uses `ScalarVisibilityOff()` (solid black); the rotated version uses the diverging LUT.
- [vtkPolyLine](https://www.vtk.org/doc/nightly/html/classvtkPolyLine.html) connects all points in order into a single polyline cell.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the elevation color legend alongside the visualization.
- [vtkTableToPolyData](https://www.vtk.org/doc/nightly/html/classvtkTableToPolyData.html) converts the table into polydata. `SetXColumn("X(m)")`, `SetYColumn("Y(m)")`, and `SetZColumn("Z(m)")` select the ECEF coordinate columns.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) is used twice. The first translates the data to the origin (centroid subtraction only). The second also rotates the centroid-translated data so that Y points North, X points East, and Z points up, using `RotateX()` and `RotateZ()` computed from the latitude mid-point.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies each transform to produce two versions of the polydata.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles both actors and the scalar bar into a single scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
