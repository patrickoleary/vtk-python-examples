### Description

This example creates a vtkExplicitStructuredGrid procedurally, converts it to an unstructured grid, and converts it back — demonstrating the round-trip conversion workflow between explicit structured and unstructured grid representations.

**Points → Cells → Explicit Structured Grid → Unstructured Grid → Explicit Structured Grid → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` outlines each cell. `LightingOff()` disables shading for a flat look. `GetProperty().SetColor()` sets the cell color.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the grid to graphics primitives.
- [vtkExplicitStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkExplicitStructuredGrid.html) represents a structured grid with explicit point coordinates and cell connectivity, supporting blanking and gaps.
- [vtkExplicitStructuredGridToUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkExplicitStructuredGridToUnstructuredGrid.html) converts the explicit structured grid to an unstructured grid, adding `BLOCK_I`, `BLOCK_J`, and `BLOCK_K` cell arrays.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) and [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) define the grid vertices and hexahedral cells.
- [vtkUnstructuredGridToExplicitStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGridToExplicitStructuredGrid.html) converts back using the `BLOCK_I/J/K` arrays to reconstruct the structured topology.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a preset camera position.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
