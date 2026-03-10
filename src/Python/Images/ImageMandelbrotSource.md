### Description

This example generates and displays a Mandelbrot fractal image using vtkImageMandelbrotSource. The source produces a 512×512 float image that is cast to unsigned char for display. It follows the VTK pipeline structure:

**ImageMandelbrotSource → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the 2D image.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts the float data to unsigned char for display.
- [vtkImageMandelbrotSource](https://www.vtk.org/doc/nightly/html/classvtkImageMandelbrotSource.html) generates a procedural Mandelbrot fractal image. `SetOriginCX()` and `SetSizeCX()` control the region of the complex plane. `SetMaximumNumberOfIterations()` controls fractal detail.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with `ParallelProjectionOn()` for correct 2D viewing.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
