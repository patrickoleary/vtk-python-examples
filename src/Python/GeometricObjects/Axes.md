### Description

This example renders a sphere alongside a 3D axes actor positioned with a user transform. It follows the standard VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAxesActor](https://www.vtk.org/doc/nightly/html/classvtkAxesActor.html) displays labeled X, Y, Z axes. `SetUserTransform()` positions the axes with the transform.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives. Connected to the source via `SetInputConnection()`.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere polygon data. `SetCenter()` and `SetRadius()` define its position and size.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a translation used to offset the axes. `Translate()` shifts the axes along the x-axis.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. `Azimuth()` and `Elevation()` adjust the viewing angle; `ResetCamera()` frames the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
