### Description

This example demonstrates boolean operations on implicit functions using vtkImplicitBoolean. A sphere is subtracted from a box (difference operation), producing a box with a spherical bite taken out of one side. The result is rendered in alice blue with steel blue edges. It follows the VTK pipeline structure:

**Sphere + Box → ImplicitBoolean → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry with `EdgeVisibilityOn()` to show the mesh wireframe.
- [vtkBox](https://www.vtk.org/doc/nightly/html/classvtkBox.html) defines an axis-aligned box with `SetBounds(-1, 1, -1, 1, -1, 1)`.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface of the boolean combination.
- [vtkImplicitBoolean](https://www.vtk.org/doc/nightly/html/classvtkImplicitBoolean.html) combines the two implicit functions. `SetOperationTypeToDifference()` subtracts the sphere from the box. Other operations include `SetOperationTypeToUnion()` and `SetOperationTypeToIntersection()`.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the boolean result on a regular 40×40×40 grid.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) defines an implicit sphere offset to the right with `SetCenter(1, 0, 0)`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
