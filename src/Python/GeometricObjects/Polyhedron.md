### Description

This example constructs a cube as a VTK_POLYHEDRON cell and renders it. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties including color to the mapped geometry.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the polyhedron to graphics primitives via `SetInputData()`.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) encodes the polyhedron topology: the number of faces followed by each face's point count and point IDs.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the eight corner vertices of the cube.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the `VTK_POLYHEDRON` cell via `InsertNextCell()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a salmon background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
