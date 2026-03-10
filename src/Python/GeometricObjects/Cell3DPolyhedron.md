### Description

This example renders a polyhedron (dodecahedron) — a generic 3D polyhedral cell defined by its vertices and face connectivity, with 20 points and 12 pentagonal faces. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) positions, orients, and colors the cell. `RotateX()` and `RotateY()` tilt it to reveal the 3D shape.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives via `SetInputData()`.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) stores lists of VTK ids.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 20 vertices of a regular dodecahedron, scaled to fit within a unit-sized bounding box.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the points and the single polyhedron cell, inserted via `InsertNextCell()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the actor into a scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
