### Description

This example demonstrates low-pass filtering with a Gaussian kernel applied to a color image (Gourds.png). The left viewport shows the original; the right shows the smoothed result. Gaussian smoothing reduces high-frequency noise while preserving the overall structure of the image. It follows the VTK pipeline structure:

**Reader → ImageCast → ImageGaussianSmooth → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to float for the Gaussian filter.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) applies a Gaussian convolution kernel. `SetStandardDeviations()` controls the blur width and `SetRadiusFactors()` controls the kernel extent.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) reads the `Gourds.png` color image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
