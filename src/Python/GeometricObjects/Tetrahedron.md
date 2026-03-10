### Description

This example constructs and renders two tetrahedra in separate vtkUnstructuredGrids that share the same point set. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns colors — cyan for the first tetrahedron, yellow for the second.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores the tetra cell, set via `SetCells()` on [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html).
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps each unstructured grid to graphics primitives via `SetInputData()`.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores eight vertices shared by both tetrahedra.
- [vtkTetra](https://www.vtk.org/doc/nightly/html/classvtkTetra.html) defines a primary 3D cell with four nonplanar points, six edges, and four triangular faces.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) represents unstructured geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark green background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
