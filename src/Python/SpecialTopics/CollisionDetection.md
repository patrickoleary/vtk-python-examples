### Description

This example detects collisions between a moving wireframe sphere and a fixed solid sphere using an animated translation.

**SphereSource × 2 → CollisionDetectionFilter → Mapper → Actor | TextActor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCollisionDetectionFilter](https://www.vtk.org/doc/nightly/html/classvtkCollisionDetectionFilter.html) finds contacting cell pairs between two inputs.
- [vtkMatrix4x4](https://www.vtk.org/doc/nightly/html/classvtkMatrix4x4.html) provides matrix4x4 functionality.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the fixed and moving sphere geometry.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) displays the collision mode and contact count.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) translates the moving sphere toward the fixed sphere.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
