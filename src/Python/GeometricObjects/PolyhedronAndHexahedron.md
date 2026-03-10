### Description

This example constructs an unstructured grid containing two cell types — a VTK_POLYHEDRON and a VTK_HEXAHEDRON — placed side-by-side using the `SetPolyhedralCells()` API. It follows the VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties including color to the mapped geometry.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) defines the cell connectivity, face definitions, and face-to-cell mapping. The polyhedron requires explicit face definitions while the hexahedron's faces are implicit.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 16 vertices shared between both cells.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) holds the cell type constants (`VTK_POLYHEDRON`, `VTK_HEXAHEDRON`).
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) assembles the mixed-cell grid via `SetPolyhedralCells()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a salmon background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
