### Description

This example displays a JPEG image as a background layer behind a 3D superquadric using two renderers on separate layers. The background renderer (layer 0) shows the image with parallel projection; the foreground renderer (layer 1) renders the interactive 3D scene. It follows the VTK pipeline structure:

**JpegReader → ImageActor → Renderer (layer 0)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the image in the background renderer.
- [vtkJPEGReader](https://www.vtk.org/doc/nightly/html/classvtkJPEGReader.html) reads the `Gourds2.jpg` JPEG image.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSuperquadricSource](https://www.vtk.org/doc/nightly/html/classvtkSuperquadricSource.html) generates a superquadric for the foreground scene.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetLayer()` create background/foreground compositing. The background renderer uses `ParallelProjectionOn()` and `InteractiveOff()`.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
