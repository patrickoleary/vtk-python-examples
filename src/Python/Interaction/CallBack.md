### Description

This example demonstrates VTK observer callbacks using both a function and a callable class. An EndInteractionEvent observer prints the camera orientation to the console after each interaction. An orientation marker widget and an outline provide scene context.

**ConeSource → Mapper → Actor + OutlineFilter → Mapper → Actor → Renderer → Window → Interactor (with callback)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAxesActor](https://www.vtk.org/doc/nightly/html/classvtkAxesActor.html) renders labeled X/Y/Z axes.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone.
- [vtkOrientationMarkerWidget](https://www.vtk.org/doc/nightly/html/classvtkOrientationMarkerWidget.html) displays an interactive axes widget in a viewport corner.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates a bounding box wireframe.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
