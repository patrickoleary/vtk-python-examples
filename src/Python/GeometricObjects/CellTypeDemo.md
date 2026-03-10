### Description

This example demonstrates all 14 cell types supported by [vtkCellTypeSource](https://www.vtk.org/doc/nightly/html/classvtkCellTypeSource.html), arranged in a labeled 4×4 grid within a single scene. Each cell type is generated, perturbed, shrunk, tessellated, and color-mapped by cell ID. It follows the standard VTK pipeline structure:

**Source → Shrink → Tessellate → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) positions each cell in the grid. 3D cells use `RotateX()` and `RotateY()` to reveal depth. `EdgeVisibilityOn()` shows wireframe edges.
- [vtkCellTypeSource](https://www.vtk.org/doc/nightly/html/classvtkCellTypeSource.html) generates a [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) for a given cell type. If a cell does not fill a rectangular area or volume, multiple cells are generated (e.g., a tetra requires 12 cells to fill a cube). `SetCellType()` selects the cell type.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the processed data to graphics primitives, using `SetScalarModeToUseCellData()` to color cells by their ID.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores integer data arrays.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) perturbs the uniform grid coordinates to make cell boundaries more visible after tessellation.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) shrinks each cell toward its centroid via `SetShrinkFactor()`, separating cells visually.
- [vtkTessellatorFilter](https://www.vtk.org/doc/nightly/html/classvtkTessellatorFilter.html) subdivides higher-order cells into linear primitives for rendering. `SetMaximumNumberOfSubdivisions()` controls the refinement level.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays text in the viewport.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles all actors and labels into a single scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
