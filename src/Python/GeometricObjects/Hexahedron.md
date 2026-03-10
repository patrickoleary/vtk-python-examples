### Description

This example constructs and renders a hexahedron — a primary 3D cell with six quadrilateral faces, twelve edges, and eight vertices. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties including color to the mapped geometry.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives via `SetInputData()`.
- [vtkHexahedron](https://www.vtk.org/doc/nightly/html/classvtkHexahedron.html) defines the cell topology by referencing the 8 point IDs.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 8 vertices of a unit hexahedron. The two faces must be in counter-clockwise order as viewed from outside.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) stores the hexahedron cell and its points.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark blue-gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
