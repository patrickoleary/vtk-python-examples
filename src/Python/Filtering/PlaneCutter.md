### Description

This example demonstrates vtkPlaneCutter to slice a sphere with a plane, producing a colored cross-section with the original sphere shown as translucent context.

**SphereSource → PlaneCutter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the cutting plane via origin and normal.
- [vtkPlaneCutter](https://www.vtk.org/doc/nightly/html/classvtkPlaneCutter.html) cuts any dataset with a vtkPlane, producing intersection geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the output to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere to be cut.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
