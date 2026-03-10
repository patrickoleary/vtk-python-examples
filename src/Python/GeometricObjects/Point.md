### Description

This example renders a single point as a vertex cell in a vtkPolyData. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties. `SetPointSize()` controls the rendered point diameter.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) defines the vertex topology referencing the point ID. The vertex cell is set via `SetVerts()` on the [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html).
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 3D coordinate of the point.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the point polydata to graphics primitives via `SetInputData()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark green background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
