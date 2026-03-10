### Description

This example cuts a cube with a plane using vtkCutter.

**Source → Cutter → Mapper → Actor | Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates the cube geometry.
- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) cuts the cube with the plane.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the cutting plane.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
