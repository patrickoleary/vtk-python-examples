### Description

This example demonstrates vtkProgrammableFilter to apply custom logic that computes a scalar field (distance from the +Z pole) on a sphere mesh.

**SphereSource → ProgrammableFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores the computed scalar values.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the output to graphics primitives with scalar coloring.
- [vtkProgrammableFilter](https://www.vtk.org/doc/nightly/html/classvtkProgrammableFilter.html) runs user-defined Python code as a VTK filter. `SetExecuteMethod()` sets the callback.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the input sphere mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
