### Description

This example demonstrates arithmetic operations on images using vtkImageMathematics. Two procedural sinusoid images — one horizontal, one vertical — are multiplied together to create an interference pattern. Three viewports show the inputs and the result side by side. It follows the VTK pipeline structure:

**Source1 + Source2 → ImageMathematics → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays each 2D image in the scene. Three actors are used for the three viewports.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts the output to unsigned char for display.
- [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) performs pixel-wise arithmetic on one or two images. `SetOperationToMultiply()` multiplies corresponding pixel values. Other operations include Add, Subtract, Divide, Invert, and many more.
- [vtkImageSinusoidSource](https://www.vtk.org/doc/nightly/html/classvtkImageSinusoidSource.html) generates procedural sinusoidal images. `SetDirection()` controls the wave orientation. `SetPeriod()` and `SetAmplitude()` control frequency and intensity.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — three renderers with `SetViewport()` create a left/center/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
