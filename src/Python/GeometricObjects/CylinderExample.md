### Description

This example demonstrates VTK's basic rendering pipeline by visualizing a cylinder. It follows the standard VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) groups the mapper with visual properties (color, orientation). `GetProperty().SetColor()` sets the surface color; `RotateX()` and `RotateY()` orient the actor in the scene.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates polygonal cylinder geometry. `SetResolution()` controls the number of circumferential facets.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives. Connected to the source via `SetInputConnection()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene from actors and manages the camera. `ResetCamera()` frames the scene, and `GetActiveCamera().Zoom()` adjusts the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
