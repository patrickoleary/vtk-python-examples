### Description

This example decimates a sphere using vtkQuadricDecimation, which uses quadric error metrics to optimally place the remaining vertices after edge collapse operations. This produces higher-quality decimated meshes than vtkDecimatePro for most inputs. Side-by-side viewports show the original mesh (left) and the 80%-reduced mesh (right). It follows the VTK pipeline structure:

**SphereSource → QuadricDecimation → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors with flat interpolation and peach-puff color, one per viewport.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized navigation.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the original and decimated meshes to graphics primitives.
- [vtkQuadricDecimation](https://www.vtk.org/doc/nightly/html/classvtkQuadricDecimation.html) reduces the polygon count by 80%. Each edge collapse places the new vertex at the position that minimizes the quadric error metric, preserving surface shape better than greedy decimation.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a high-resolution tessellated sphere with 40×40 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
