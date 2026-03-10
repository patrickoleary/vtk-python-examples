### Description

This example cuts a sphere with multiple planes and display the resulting polylines using vtkCutter and vtkStripper.

**Source → Cutter → Stripper → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) cuts the sphere to produce contour lines at each plane.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit cutting planes.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the sphere and polylines to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the input sphere polydata.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) joins contour line segments into continuous polylines.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
