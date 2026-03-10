### Description

This example extracts the outer surface of a hexahedron and cut it with a plane.

**Hexahedron → DataSetSurfaceFilter → Mapper → Actor | Cutter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) cuts the surface with the plane.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the dataset to graphics primitives.
- [vtkDataSetSurfaceFilter](https://www.vtk.org/doc/nightly/html/classvtkDataSetSurfaceFilter.html) extracts the outer polygonal surface.
- [vtkHexahedron](https://www.vtk.org/doc/nightly/html/classvtkHexahedron.html) defines the hexahedral cell.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the cutting plane.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) stores the unstructured grid.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
