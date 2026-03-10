### Description

This example renders a single vertex at the origin using vtkVertex — a primary zero-dimensional cell defined by one point. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties. `SetPointSize()` controls the rendered point diameter.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores the vertex cell, set via `SetVerts()` on [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html).
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the single 3D coordinate.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the vertex to graphics primitives via `SetInputData()`.
- [vtkVertex](https://www.vtk.org/doc/nightly/html/classvtkVertex.html) defines the vertex cell by referencing the point ID.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark green background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
