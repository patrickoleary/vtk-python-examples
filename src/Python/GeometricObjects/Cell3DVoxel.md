### Description

This example renders a voxel — an axis-aligned hexahedron used on regular grids, defined by 8 explicit point coordinates. Unlike a hexahedron, a voxel uses a specific point ordering where the i-index varies fastest. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) positions, orients, and colors the cell. `RotateX()` and `RotateY()` tilt it to reveal the 3D shape.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives via `SetInputData()`.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 8 vertices of a unit voxel centered at the origin.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the points and the single cell, inserted via `InsertNextCell()`.
- [vtkVoxel](https://www.vtk.org/doc/nightly/html/classvtkVoxel.html) defines the voxel cell by mapping 8 point IDs via `GetPointIds().SetId()`. The point ordering differs from vtkHexahedron — points are ordered with i varying fastest, then j, then k.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the actor into a scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
