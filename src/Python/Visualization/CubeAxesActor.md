### Description

This example displays labeled cube axes with gridlines around a superquadric surface.

**Source → Mapper → Actor → CubeAxes → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry with diffuse and specular shading.
- [vtkCubeAxesActor](https://www.vtk.org/doc/nightly/html/classvtkCubeAxesActor.html) draws labeled bounding-box axes with gridlines.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSuperquadricSource](https://www.vtk.org/doc/nightly/html/classvtkSuperquadricSource.html) generates superquadric polygon data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
