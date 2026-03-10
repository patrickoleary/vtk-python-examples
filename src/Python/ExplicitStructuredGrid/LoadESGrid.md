### Description

This example loads the [UNISIM-II-D reservoir model](https://www.unisim.cepetro.unicamp.br/benchmarks/en/unisim-ii/unisim-ii-d) from a VTU file, converts it to a vtkExplicitStructuredGrid, computes face connectivity flags, and colors the cells by their connectivity status.

**Reader → Convert to Explicit Structured Grid → Connectivity Flags → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` outlines each cell to reveal the grid structure.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the grid to graphics primitives, colored by the connectivity flags scalar range.
- [vtkUnstructuredGridToExplicitStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGridToExplicitStructuredGrid.html) converts the unstructured grid to an explicit structured grid using the block index arrays.
- [vtkXMLUnstructuredGridReader](https://www.vtk.org/doc/nightly/html/classvtkXMLUnstructuredGridReader.html) reads the reservoir model from a `.vtu` file containing `BLOCK_I`, `BLOCK_J`, and `BLOCK_K` cell arrays.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a preset camera position suited to the reservoir model coordinates.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
