### Description

This example displays four geometric objects in a 2×2 grid of viewports sharing one camera.

**Sources → Mappers → Actors → Renderers → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates cone polygon data.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates cube polygon data.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates cylinder polygon data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere polygon data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles each viewport and shares one camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
