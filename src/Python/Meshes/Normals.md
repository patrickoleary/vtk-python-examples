### Description

This example computes and visualizes surface normals on a low-resolution sphere using vtkPolyDataNormals. Side-by-side viewports show the sphere without normals using flat shading (left) and with computed normals using smooth Phong shading (right). Computing point normals allows the renderer to interpolate lighting across faces for a smooth appearance. It follows the VTK pipeline structure:

**SphereSource → PolyDataNormals → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the left uses `SetInterpolationToFlat()`, the right uses `SetInterpolationToPhong()` with computed normals.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized navigation.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps both the flat and smooth meshes to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes point normals from the mesh topology. `SetFeatureAngle(60.0)` controls when edges are considered sharp. `SplittingOff()` prevents vertex duplication at sharp edges.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a low-resolution sphere with 12×12 resolution to emphasize the difference between flat and smooth shading.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
