### Description

This example demonstrates keypress event handling with an observer callback. Press 's' to toggle between wireframe and surface representation, 'c' to cycle through colors, and 'q' to quit.

**ConeSource → Mapper → Actor → Renderer → Window → Interactor (with keypress callback)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) provides default mouse interaction.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
