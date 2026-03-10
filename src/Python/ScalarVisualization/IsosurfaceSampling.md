### Description

This example samples a cylinder field onto a sphere isosurface using vtkProbeFilter.

**Sphere → SampleFunction → FlyingEdges3D | Cylinder → SampleFunction → ProbeFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCylinder](https://www.vtk.org/doc/nightly/html/classvtkCylinder.html) defines the cylinder implicit function.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts the sphere isosurface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkProbeFilter](https://www.vtk.org/doc/nightly/html/classvtkProbeFilter.html) probes the cylinder field onto the sphere surface.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) samples implicit functions on a regular grid.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) defines the sphere implicit function.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
