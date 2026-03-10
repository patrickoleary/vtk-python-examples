### Description

This example visualizes a rectilinear grid by shrinking each cell to reveal the grid structure. A 2x3x2 grid with non-uniform spacing is created and displayed with shrunk cells.

**RectilinearGrid → ShrinkFilter → DataSetMapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps any dataset type to graphics primitives.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores the coordinate values along each axis.
- [vtkRectilinearGrid](https://www.vtk.org/doc/nightly/html/classvtkRectilinearGrid.html) defines a grid with non-uniform spacing along each axis.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) shrinks each cell toward its centroid to reveal grid structure.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
