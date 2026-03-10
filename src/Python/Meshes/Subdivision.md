### Description

This example subdivides an icosahedron using vtkLoopSubdivisionFilter, which applies Loop subdivision to increase mesh density and smooth the geometry. Side-by-side viewports show the original coarse mesh (left) and the subdivided smooth mesh (right), both with visible edges. It follows the VTK pipeline structure:

**PlatonicSolidSource → LoopSubdivisionFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors with alice-blue faces and steel-blue edges, one per viewport.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized navigation.
- [vtkLoopSubdivisionFilter](https://www.vtk.org/doc/nightly/html/classvtkLoopSubdivisionFilter.html) applies 3 iterations of Loop subdivision. Each iteration splits every triangle into four, smoothing vertex positions using a weighted average of neighbors.
- [vtkPlatonicSolidSource](https://www.vtk.org/doc/nightly/html/classvtkPlatonicSolidSource.html) generates an icosahedron (20-face platonic solid) as the coarse input mesh.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the original and subdivided meshes to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
