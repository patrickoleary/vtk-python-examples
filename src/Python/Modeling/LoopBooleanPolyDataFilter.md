### Description

This example demonstrates vtkLoopBooleanPolyDataFilter to compute the boolean intersection of two overlapping spheres, with the original spheres shown as translucent context.

**SphereSource A + SphereSource B → LoopBooleanPolyDataFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `SetOpacity()` makes the context spheres translucent.
- [vtkLoopBooleanPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkLoopBooleanPolyDataFilter.html) performs boolean union, intersection, or difference on two closed polydata surfaces.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the boolean result and context geometry to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the two input spheres.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
