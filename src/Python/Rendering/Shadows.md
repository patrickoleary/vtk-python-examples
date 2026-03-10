### Description

This example renders a sphere on a ground plane with shadow mapping using two lights (a warm overhead sun and a cool tungsten fill).

**Source → Mapper → Actor → ShadowMapPass → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCameraPass](https://www.vtk.org/doc/nightly/html/classvtkCameraPass.html) sets up the camera projection for the shadow map render passes.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates the ground plane geometry.
- [vtkLight](https://www.vtk.org/doc/nightly/html/classvtkLight.html) provides the warm sun and cool fill lights that cast shadows.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkRenderPassCollection](https://www.vtk.org/doc/nightly/html/classvtkRenderPassCollection.html) collects render passes into a sequence.
- [vtkSequencePass](https://www.vtk.org/doc/nightly/html/classvtkSequencePass.html) executes the collected render passes in order.
- [vtkShadowMapPass](https://www.vtk.org/doc/nightly/html/classvtkShadowMapPass.html) generates shadow maps from the scene lights.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere polygon data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
