### Description

This example constructs and renders a dodecahedron as a vtkPolyhedron — a general polyhedral cell defined by its vertices and face connectivity. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties including color to the mapped geometry.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polyhedron surface to graphics primitives via `SetInputData()`.
- [vtkPolyhedron](https://www.vtk.org/doc/nightly/html/classvtkPolyhedron.html) represents a general 3D polyhedral cell. Point IDs and coordinates are inserted via `GetPointIds().InsertNextId()` and `GetPoints().InsertNextPoint()`. Face connectivity is provided as a flat list to `SetFaces()`, followed by `Initialize()`. `GetPolyData()` extracts a renderable surface.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a cadet blue background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
