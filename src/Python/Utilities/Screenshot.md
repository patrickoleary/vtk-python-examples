### Description

This example captures a render window to a PNG image file. The vtkWindowToImageFilter reads the framebuffer contents and produces a vtkImageData, which is then written to disk by vtkPNGWriter.

**SphereSource → Mapper → Actor → Renderer → RenderWindow → WindowToImageFilter → PNGWriter**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPNGWriter](https://www.vtk.org/doc/nightly/html/classvtkPNGWriter.html) writes the captured image to a PNG file.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere geometry.
- [vtkWindowToImageFilter](https://www.vtk.org/doc/nightly/html/classvtkWindowToImageFilter.html) captures the render window framebuffer as image data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
