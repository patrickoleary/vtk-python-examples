### Description

This example converts DG cell grids to unstructured grids using vtkCellGridToUnstructuredGrid. Four DG cell types (tetrahedron, hexahedron, wedge, pyramid) are generated with vtkCellGridCellSource and converted to standard VTK unstructured grids for rendering. It follows the VTK pipeline structure:

**CellGridCellSource → CellGridToUnstructuredGrid → DataSetMapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Four actors display each cell type with distinct colors and edge visibility.
- [vtkCellGridCellSource](https://www.vtk.org/doc/nightly/html/classvtkCellGridCellSource.html) generates a single DG cell of the specified type. `SetCellType()` accepts type names such as `"vtkDGTet"`, `"vtkDGHex"`, `"vtkDGWdg"`, and `"vtkDGPyr"`.
- [vtkCellGridToUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkCellGridToUnstructuredGrid.html) converts a cell grid to a conventional vtkUnstructuredGrid so it can be rendered with standard mappers.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
