### Description

This example visualizes a planes-intersection test with two boxes. A sphere is rendered alongside an overlapping wireframe box (green — intersects) and a displaced wireframe box (red — does not intersect). It follows the VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties — semi-transparent cornsilk for the sphere, green wireframe for the intersecting box, and red wireframe for the non-intersecting box.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates wireframe boxes for visualization — one matching the sphere's bounds (overlapping) and one offset away (displaced).
- [vtkPlanesIntersection](https://www.vtk.org/doc/nightly/html/classvtkPlanesIntersection.html) creates a set of planes from the sphere's bounds and tests whether each box region intersects them via `IntersectsRegion()`.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the sphere and both boxes to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a unit sphere. Its bounding box is extracted with `GetBounds()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a slate gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
