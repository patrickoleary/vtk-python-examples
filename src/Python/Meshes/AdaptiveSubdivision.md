### Description

This example adaptively subdivides a coarse sphere mesh so that no triangle edge exceeds a specified maximum length, using vtkAdaptiveSubdivisionFilter. The left viewport shows the original coarse wireframe mesh and the right viewport shows the adaptively subdivided result with many more triangles where edges were long. It follows the VTK pipeline structure:

**SphereSource → TriangleFilter → AdaptiveSubdivisionFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the original and subdivided meshes as wireframes via `SetRepresentationToWireframe()`.
- [vtkAdaptiveSubdivisionFilter](https://www.vtk.org/doc/nightly/html/classvtkAdaptiveSubdivisionFilter.html) subdivides triangles whose edges exceed a threshold length. `SetMaximumEdgeLength(0.2)` ensures all output edges are shorter than 0.2 world units. Unlike uniform subdivision, this concentrates new triangles only where needed.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a coarse sphere with low resolution (`SetPhiResolution(6)`, `SetThetaResolution(6)`).
- [vtkTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkTriangleFilter.html) converts all polygons to triangles, which is required by vtkAdaptiveSubdivisionFilter.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout. Cameras are shared so both viewports rotate together.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
