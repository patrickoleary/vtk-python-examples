### Description

This example computes a distance field from a polydata surface using vtkImplicitModeller and extracts an isosurface at a fixed distance to show the distance envelope around the original geometry. A grey sphere is surrounded by a translucent tomato red envelope at distance 0.25. It follows the VTK pipeline structure:

**SphereSource → ImplicitModeller → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors are used: the translucent distance envelope in tomato red and the opaque original sphere in grey.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the isosurface at distance 0.25 — the set of all points at exactly that distance from the sphere surface.
- [vtkImplicitModeller](https://www.vtk.org/doc/nightly/html/classvtkImplicitModeller.html) computes a distance field on a regular grid around the input polydata. Each voxel stores the distance to the nearest point on the surface. `SetMaximumDistance(0.5)` limits computation to voxels within that distance.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps both the envelope and original sphere to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere as the input geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
