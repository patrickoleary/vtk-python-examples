### Description

This example displays a movable text overlay on a sphere using an interactive text widget.

**SphereSource → Mapper → Actor + TextWidget → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere polygon data.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) renders the text string.
- [vtkTextRepresentation](https://www.vtk.org/doc/nightly/html/classvtkTextRepresentation.html) controls the position and size of the text widget.
- [vtkTextWidget](https://www.vtk.org/doc/nightly/html/classvtkTextWidget.html) provides an interactive, repositionable text overlay.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
