### Description

This example demonstrates vtkVolumeOfRevolutionFilter to revolve a 2D polyline profile around the Y axis, creating a vase-like 3D solid.

**PolyLine → VolumeOfRevolutionFilter → DataSetSurfaceFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkDataSetSurfaceFilter](https://www.vtk.org/doc/nightly/html/classvtkDataSetSurfaceFilter.html) extracts the surface geometry from the unstructured grid output.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface to graphics primitives.
- [vtkVolumeOfRevolutionFilter](https://www.vtk.org/doc/nightly/html/classvtkVolumeOfRevolutionFilter.html) revolves a 2D profile around an axis to produce a 3D unstructured grid.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
