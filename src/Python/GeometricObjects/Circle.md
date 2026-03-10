### Description

This example draws a circle by approximating it as a regular polygon with many sides. It follows the standard VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties including color to the mapped geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives. Connected to the source via `SetInputConnection()`.
- [vtkRegularPolygonSource](https://www.vtk.org/doc/nightly/html/classvtkRegularPolygonSource.html) generates a polygon with `SetNumberOfSides(50)` to approximate a circle. `GeneratePolygonOff()` produces only the outline; comment it out to generate a filled disk. `SetRadius()` and `SetCenter()` control the geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark green background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
