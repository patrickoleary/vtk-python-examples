### Description

This example generates and displays a sinusoidal pattern image using vtkImageSinusoidSource. The source produces a 256×256 double image with a diagonal wave pattern that is cast to unsigned char for display. It follows the VTK pipeline structure:

**ImageSinusoidSource → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the 2D image.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts the double data to unsigned char for display.
- [vtkImageSinusoidSource](https://www.vtk.org/doc/nightly/html/classvtkImageSinusoidSource.html) generates a procedural sinusoidal image. `SetDirection()` controls the wave orientation, `SetPeriod()` the wavelength, and `SetAmplitude()` the intensity range.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with `ParallelProjectionOn()` for correct 2D viewing.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
