### Description

This example creates a structured grid and blank a point. The blanked point and its surrounding faces are removed from the visualization using a geometry filter.

**StructuredGrid → StructuredGridGeometryFilter → DataSetMapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps any dataset type to graphics primitives.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 3D coordinates for each grid point.
- [vtkStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkStructuredGrid.html) defines a topologically regular grid with arbitrary point positions.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts surface geometry, respecting blanked points.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
