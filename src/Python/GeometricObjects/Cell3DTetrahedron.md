### Description

This example renders a tetrahedron — a 3D cell with four triangular faces, defined by 4 explicit point coordinates. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) positions, orients, and colors the cell. `RotateX()` and `RotateY()` tilt it to reveal the 3D shape.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) collects the cell for insertion into the grid.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives via `SetInputData()`.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 4 vertices of a tetrahedron.
- [vtkTetra](https://www.vtk.org/doc/nightly/html/classvtkTetra.html) defines the tetrahedron cell by mapping 4 point IDs via `GetPointIds().SetId()`.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the points and the single cell, set via `SetCells(VTK_TETRA, cells)`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the actor into a scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
