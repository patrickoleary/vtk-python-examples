### Description

This example applies a custom 3×3 sharpening convolution kernel to a grayscale image using vtkImageConvolve and displays the original and filtered images side by side. It follows the VTK pipeline structure:

**PNGReader → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageConvolve](https://www.vtk.org/doc/nightly/html/classvtkImageConvolve.html) applies a user-defined 3×3 convolution kernel. The sharpening kernel (center=5, neighbors=-1) enhances edges while preserving brightness.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) reads the `Gourds.png` image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
