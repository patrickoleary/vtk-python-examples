### Description

This example displays a "Hello World!" text overlay using vtkTextActor — a 2D annotation that renders styled text at a fixed screen position. It follows the VTK pipeline structure:

**TextActor → Renderer → Window → Interactor**

- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) creates a 2D text overlay. `SetInput()` sets the string and `SetDisplayPosition()` places it in pixel coordinates.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark green background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
