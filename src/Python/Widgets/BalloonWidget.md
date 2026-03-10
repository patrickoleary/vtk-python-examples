### Description

This example displays balloon popup text when hovering over actors in the scene.

**SphereSource / RegularPolygonSource → Mapper → Actor → BalloonWidget → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkBalloonRepresentation](https://www.vtk.org/doc/nightly/html/classvtkBalloonRepresentation.html) controls the layout and appearance of the balloon popup.
- [vtkBalloonWidget](https://www.vtk.org/doc/nightly/html/classvtkBalloonWidget.html) displays tooltip text when the mouse hovers over an actor.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRegularPolygonSource](https://www.vtk.org/doc/nightly/html/classvtkRegularPolygonSource.html) generates a regular polygon.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere polygon data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
