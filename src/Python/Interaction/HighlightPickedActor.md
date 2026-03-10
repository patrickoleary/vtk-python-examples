### Description

This example demonstrates actor picking with vtkCellPicker. Click on any of the three objects (sphere, cube, cone) to highlight it in yellow; the previously highlighted actor reverts to its original color.

**Sources → Mappers → Actors → Renderer → Window → Interactor (with pick callback)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellPicker](https://www.vtk.org/doc/nightly/html/classvtkCellPicker.html) performs cell-level picking to identify the actor under the mouse.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a cube.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) maps mouse motion to camera transformations.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html), [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html), [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generate the pickable objects.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
