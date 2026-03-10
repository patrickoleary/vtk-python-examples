### Description

This example reads UTM coordinates and elevation from a CSV file using pandas and numpy, builds a polyline, and renders it colored by elevation with an orientation marker widget. It demonstrates interoperability between pandas, numpy, and VTK:

**CSV → pandas → numpy → numpy_to_vtk → vtkPolyData → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Scalar coloring from the elevation array drives the line appearance.
- [vtkAxesActor](https://www.vtk.org/doc/nightly/html/classvtkAxesActor.html) displays labeled X, Y, Z axes. `SetXAxisLabelText("East")`, `SetYAxisLabelText("North")`, and `SetZAxisLabelText("Zenith")` label the UTM coordinate axes.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps elevation values to colors. `SetHueRange(0.667, 0.0)` creates a simple blue-to-red ramp.
- [vtkOrientationMarkerWidget](https://www.vtk.org/doc/nightly/html/classvtkOrientationMarkerWidget.html) places the labeled axes in the lower-left corner of the render window. `SetViewport()` controls its size and position.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the UTM coordinates as 3D points. `SetData()` accepts the converted numpy array directly.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) assembles the points, scalars, and line cells into a dataset.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives with scalar coloring enabled.
- [vtkPolyLine](https://www.vtk.org/doc/nightly/html/classvtkPolyLine.html) connects all points in order into a single polyline cell.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the elevation color legend alongside the visualization.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
