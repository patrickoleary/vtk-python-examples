### Description

This example embeds a VTK render window inside a PyQt6 application. A sphere is displayed in the VTK viewport within a QMainWindow. Uses QOpenGLWidget as the render window interactor base for macOS compatibility.

**SphereSource → Mapper → Actor → Renderer → RenderWindow → QVTKRenderWindowInteractor → QMainWindow**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere polygon data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
