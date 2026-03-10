### Description

This example triangulates a cylinder (which has quad faces and polygon caps) using vtkTriangleFilter and displays the original and triangulated meshes side by side with visible edges to show the difference in face topology.

**CylinderSource → Original Mapper + TriangleFilter → Triangulated Mapper → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` reveals cell boundaries; `SetPosition()` offsets the two meshes for side-by-side comparison.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates a cylinder whose body is made of quadrilateral faces and whose caps are polygonal fans.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the original and triangulated meshes to graphics primitives.
- [vtkTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkTriangleFilter.html) converts all polygonal cells (quads, polygons) to triangles, which is a common requirement for many downstream algorithms.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. `ResetCamera()` frames both meshes.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
