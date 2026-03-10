### Description

This example demonstrates shadow-mapped spotlights illuminating a box, cone, and sphere on a ground plane.

**PlaneSource + CubeSource + ConeSource + SphereSource → Mapper → Actor | ShadowMapPass + Lights → OpenGLRenderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCameraPass](https://www.vtk.org/doc/nightly/html/classvtkCameraPass.html) provides camera pass functionality.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a cube.
- [vtkLight](https://www.vtk.org/doc/nightly/html/classvtkLight.html) defines positional spotlights aimed at scene objects.
- [vtkLightActor](https://www.vtk.org/doc/nightly/html/classvtkLightActor.html) displays light frustum wireframes.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkOpaquePass](https://www.vtk.org/doc/nightly/html/classvtkOpaquePass.html) provides opaque pass functionality.
- [vtkOpenGLRenderer](https://www.vtk.org/doc/nightly/html/classvtkOpenGLRenderer.html) supports custom render pass pipelines.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates a plane.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes point and/or cell normals.
- [vtkRenderPassCollection](https://www.vtk.org/doc/nightly/html/classvtkRenderPassCollection.html) provides render pass collection functionality.
- [vtkSequencePass](https://www.vtk.org/doc/nightly/html/classvtkSequencePass.html) provides sequence pass functionality.
- [vtkShadowMapPass](https://www.vtk.org/doc/nightly/html/classvtkShadowMapPass.html) renders shadow maps from each positional light.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
