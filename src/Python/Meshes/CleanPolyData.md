### Description

This example removes duplicate points and degenerate cells from a mesh using vtkCleanPolyData. The same sphere is appended to itself three times, tripling the point and cell count. The left viewport shows the uncleaned mesh where triplicated overlapping faces cause visible z-fighting artifacts; the right viewport shows the cleaned mesh reduced back to a single clean copy. Text overlays display the point and cell counts in each viewport. It follows the VTK pipeline structure:

**SphereSource → AppendPolyData (×3) → CleanPolyData → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors with alice-blue faces and steel-blue edges, one per viewport.
- [vtkAppendPolyData](https://www.vtk.org/doc/nightly/html/classvtkAppendPolyData.html) appends the same sphere three times, creating triple-duplicate points and faces that cause z-fighting.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized navigation.
- [vtkCleanPolyData](https://www.vtk.org/doc/nightly/html/classvtkCleanPolyData.html) merges coincident points (tolerance 0.0) and removes the resulting degenerate duplicate cells, restoring the mesh to a single clean copy.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the uncleaned and cleaned meshes to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a single tessellated sphere with 20×20 resolution.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays point and cell counts in each viewport.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
