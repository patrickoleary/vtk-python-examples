### Description

This example renders two cones with different material properties (one using GetProperty(), the other via an explicit vtkProperty), then animate 60 frames of azimuth rotation before entering interactive mode.

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates the cone polygon data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cone polygon data to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) controls surface appearance (colour, specular, diffuse) on one of the cones.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
