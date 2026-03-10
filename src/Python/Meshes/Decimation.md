### Description

This example decimates a sphere using vtkDecimatePro with a 90% target reduction. Side-by-side viewports show the original mesh (left) and the decimated mesh (right), both with flat shading and gold back-faces. `PreserveTopologyOn()` ensures the decimated mesh remains a valid manifold. It follows the VTK pipeline structure:

**SphereSource → DecimatePro → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors with flat interpolation and navajo-white color, one per viewport.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized navigation.
- [vtkDecimatePro](https://www.vtk.org/doc/nightly/html/classvtkDecimatePro.html) reduces the polygon count by 90%. `SetTargetReduction(0.9)` specifies that 90% of triangles should be removed. `PreserveTopologyOn()` prevents the mesh from developing holes or non-manifold edges.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the original and decimated meshes to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) creates a gold back-face property shared by both actors.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere with 30×15 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
