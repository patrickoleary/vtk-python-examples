### Description

This example renders Earth continent outlines on a sphere using vtkEarthSource. It follows the standard VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties — black for the continent outlines, peach puff for the sphere surface.
- [vtkEarthSource](https://www.vtk.org/doc/nightly/html/classvtkEarthSource.html) generates polygonal continent outlines at a given radius. `OutlineOn()` produces outline polylines rather than filled polygons. `GetRadius()` returns the sphere radius used by the source.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each source to graphics primitives via `SetInputConnection()`.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere matching the Earth source radius as a background surface. `SetThetaResolution()` and `SetPhiResolution()` control the mesh density.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a black background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
