### Description

This example computes a weighted sum of a Mandelbrot fractal image and a sinusoidal image using vtkImageWeightedSum and displays all three side by side. The Mandelbrot image is weighted at 0.8 and the sinusoid at 0.2. It follows the VTK pipeline structure:

**Source1 + Source2 → ImageWeightedSum → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays each 2D image in the scene. Three actors are used for the three viewports.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts each output to unsigned char for display.
- [vtkImageMandelbrotSource](https://www.vtk.org/doc/nightly/html/classvtkImageMandelbrotSource.html) generates a Mandelbrot fractal image as the first input.
- [vtkImageSinusoidSource](https://www.vtk.org/doc/nightly/html/classvtkImageSinusoidSource.html) generates a sinusoidal image as the second input.
- [vtkImageWeightedSum](https://www.vtk.org/doc/nightly/html/classvtkImageWeightedSum.html) computes the weighted sum of multiple images. `AddInputConnection()` adds each image and `SetWeight()` assigns its contribution. Images must have the same extent and scalar type.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — three renderers with `SetViewport()` create a left/center/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
