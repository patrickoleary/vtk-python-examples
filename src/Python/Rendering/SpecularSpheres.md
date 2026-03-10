### Description

This example demonstrates the effect of specular power on a row of eight spheres. Top row: specular=1.0, power doubles from 5 to 640. Bottom row: specular=0.5, power doubles from 5 to 640.

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with varying specular power.
- [vtkLight](https://www.vtk.org/doc/nightly/html/classvtkLight.html) provides scene lighting for the specular demonstration.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the sphere polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a high-resolution sphere shared by all actors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
