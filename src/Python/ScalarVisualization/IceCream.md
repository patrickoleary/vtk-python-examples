### Description

This example models an ice cream cone using boolean combinations of implicit functions.

**ImplicitBoolean → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCone](https://www.vtk.org/doc/nightly/html/classvtkCone.html) defines the cone implicit function.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts isosurfaces from the sampled fields.
- [vtkImplicitBoolean](https://www.vtk.org/doc/nightly/html/classvtkImplicitBoolean.html) combines primitives with boolean operations.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) clips the cone to finite extent.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) samples the implicit functions on a regular grid.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) defines the ice cream scoop and bite.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
