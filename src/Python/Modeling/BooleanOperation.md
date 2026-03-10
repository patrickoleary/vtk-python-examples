### Description

This example demonstrates boolean operations (union, intersection, difference) on two overlapping spheres using vtkBooleanOperationPolyDataFilter. Three side-by-side viewports show one operation each, all rendered in banana yellow. It follows the VTK pipeline structure:

**SphereSource (×2) → BooleanOperationPolyDataFilter (×3) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays each result in banana yellow.
- [vtkBooleanOperationPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkBooleanOperationPolyDataFilter.html) performs union, intersection, and difference operations on the two sphere surfaces.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each boolean result to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates two overlapping spheres offset along the X axis with 40-sided resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — three renderers in side-by-side viewports sharing one camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
