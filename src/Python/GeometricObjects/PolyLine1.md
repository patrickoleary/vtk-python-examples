### Description

This example draws a closed hexagonal polyline through six vertices using vtkCellArray line cells. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties including color to the mapped geometry.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) defines a closed polyline by inserting seven point IDs (returning to the first point). The cell is set via `SetLines()` on [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html).
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores six vertices arranged as a regular hexagon.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polyline to graphics primitives via `SetInputData()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark blue background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
