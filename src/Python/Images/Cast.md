### Description

This example generates a Mandelbrot fractal image (float scalars) and casts it to unsigned char for display using vtkImageCast. It follows the VTK pipeline structure:

**ImageMandelbrotSource → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the 2D image.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts the float data to unsigned char for display.
- [vtkImageMandelbrotSource](https://www.vtk.org/doc/nightly/html/classvtkImageMandelbrotSource.html) generates a procedural Mandelbrot fractal image with float scalars.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with `ParallelProjectionOn()` for correct 2D viewing.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
