### Description

This example demonstrates eight 3D linear cell types arranged in a labeled grid within a single scene. The point coordinates for each cell type are normalized to approximately 1³ unit size for uniform display. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) positions, orients, and colors each cell. `RotateX()` and `RotateY()` tilt each cell to reveal its 3D shape. `SetPosition()` places it in the grid.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps each unstructured grid to graphics primitives via `SetInputData()`.
- [vtkHexagonalPrism](https://www.vtk.org/doc/nightly/html/classvtkHexagonalPrism.html) — a prism with two hexagonal faces and six rectangular sides (12 points).
- [vtkHexahedron](https://www.vtk.org/doc/nightly/html/classvtkHexahedron.html) — a cube or brick with six quadrilateral faces (8 points).
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) stores lists of VTK ids.
- [vtkPentagonalPrism](https://www.vtk.org/doc/nightly/html/classvtkPentagonalPrism.html) — a prism with two pentagonal faces and five rectangular sides (10 points).
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPyramid](https://www.vtk.org/doc/nightly/html/classvtkPyramid.html) — a square base tapering to an apex (5 points).
- [vtkTetra](https://www.vtk.org/doc/nightly/html/classvtkTetra.html) — a tetrahedron with four triangular faces (4 points).
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays text in the viewport.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) represents unstructured geometry.
- [vtkVoxel](https://www.vtk.org/doc/nightly/html/classvtkVoxel.html) — an axis-aligned hexahedron on a regular grid (8 points).
- [vtkWedge](https://www.vtk.org/doc/nightly/html/classvtkWedge.html) — two triangular ends joined by three rectangular faces (6 points).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles all actors and labels into a single scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
