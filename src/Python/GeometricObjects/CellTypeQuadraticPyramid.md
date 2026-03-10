### Description

This example demonstrates [vtkCellTypeSource](https://www.vtk.org/doc/nightly/html/classvtkCellTypeSource.html) for the Quadratic Pyramid cell type. The source generates an unstructured grid of quadratic pyramid cells, which are perturbed, shrunk, and color-mapped by cell ID. It follows the standard VTK pipeline structure:

**Source → Shrink → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties. `EdgeVisibilityOn()` shows wireframe edges. `RotateX()` and `RotateY()` tilt the 3D shape.
- [vtkCellTypeSource](https://www.vtk.org/doc/nightly/html/classvtkCellTypeSource.html) generates a [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) of quadratic pyramid cells via `SetCellType()`.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the data to graphics primitives, coloring by cell ID.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores integer data arrays.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) perturbs coordinates to make cell boundaries visible.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) shrinks each cell toward its centroid via `SetShrinkFactor()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
