### Description

This example connects several points with individual vtkLine segments stored in a vtkPolyData. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties. `SetLineWidth()` controls the rendered line thickness.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) defines each line segment between consecutive points, inserted into a [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html).
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the path vertices.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) assembles the points and line cells.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the line polydata to graphics primitives via `SetInputData()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a silver background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
