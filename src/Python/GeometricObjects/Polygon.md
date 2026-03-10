### Description

This example renders a quadrilateral polygon using vtkPolygon. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties including color to the mapped geometry.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores the polygon cell, set via `SetPolys()` on [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html).
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the four corner vertices.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon to graphics primitives via `SetInputData()`.
- [vtkPolygon](https://www.vtk.org/doc/nightly/html/classvtkPolygon.html) defines the polygon cell by referencing point IDs in counterclockwise order. The polygon normal is implicitly defined via the right-hand rule.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a salmon background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
