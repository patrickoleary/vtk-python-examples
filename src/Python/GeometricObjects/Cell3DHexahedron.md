### Description

This example renders a hexahedron (brick/cube) — a 3D cell with six quadrilateral faces, defined by 8 explicit point coordinates. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) positions, orients, and colors the cell. `RotateX()` and `RotateY()` tilt it to reveal the 3D shape.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives via `SetInputData()`.
- [vtkHexahedron](https://www.vtk.org/doc/nightly/html/classvtkHexahedron.html) defines the hexahedron cell by mapping 8 point IDs via `GetPointIds().SetId()`.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 8 vertices of a unit cube centered at the origin.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the points and the single cell, inserted via `InsertNextCell()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the actor into a scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
