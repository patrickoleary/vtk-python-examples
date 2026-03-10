### Description

This example displays two lines from a common origin, each with a different color assigned via per-cell scalar data. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) sets `SetLineWidth(4)` for visibility.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) collects the line cells.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) defines each line segment by referencing point indices via `GetPointIds().SetId()`.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores three points: an origin and two endpoints.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) assembles the points, lines, and cell colors into a single dataset.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives via `SetInputData()`.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) holds per-cell RGB colors (unsigned char tuples). Each color is associated with the line at the same index via `GetCellData().SetScalars()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a slate gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
