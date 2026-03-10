### Description

This example clips a plane with a boolean combination of a sphere and a cylinder.

**Source → ImplicitBoolean → ClipPolyData → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkClipPolyData](https://www.vtk.org/doc/nightly/html/classvtkClipPolyData.html) clips the plane with the boolean function.
- [vtkCylinder](https://www.vtk.org/doc/nightly/html/classvtkCylinder.html) defines the cylinder implicit function.
- [vtkImplicitBoolean](https://www.vtk.org/doc/nightly/html/classvtkImplicitBoolean.html) combines the implicit functions with a boolean union.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates the plane geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) defines the sphere implicit function.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) positions the sphere and cylinder.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
