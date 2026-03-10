### Description

This example creates a structured grid of a semi-cylinder. Vectors proportional to radius and oriented in the tangential direction are displayed using a hedgehog filter.

**StructuredGrid → HedgeHog → Mapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores the vector data associated with each point.
- [vtkHedgeHog](https://www.vtk.org/doc/nightly/html/classvtkHedgeHog.html) creates oriented lines from vector data at each point.
- [vtkMath](https://www.vtk.org/doc/nightly/html/classvtkMath.html) provides the radians-from-degrees conversion.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 3D coordinates for each grid point.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkStructuredGrid.html) defines a topologically regular grid with arbitrary point positions.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
