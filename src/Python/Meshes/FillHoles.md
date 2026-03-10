### Description

This example fills holes in a mesh using vtkFillHolesFilter. Cells are removed from a sphere to create holes, then the filter patches them with new triangles. Side-by-side viewports show the mesh with holes (left) and the repaired mesh (right). It follows the VTK pipeline structure:

**SphereSource → Cell Removal → FillHolesFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors with peach-puff faces and steel-blue edges, one per viewport.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized navigation.
- [vtkFillHolesFilter](https://www.vtk.org/doc/nightly/html/classvtkFillHolesFilter.html) identifies boundary edge loops and fills them with new triangles. `SetHoleSize()` controls the maximum hole size to fill.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the holed and repaired meshes to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere with 20×20 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
