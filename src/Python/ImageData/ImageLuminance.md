### Description

This example converts an RGB color image (Gourds.png) to grayscale using vtkImageLuminance. The left viewport shows the original color image; the right shows the grayscale luminance result. vtkImageLuminance computes luminance as 0.30×R + 0.59×G + 0.11×B, matching the human eye's sensitivity to color channels. It follows the VTK pipeline structure:

**Reader → ImageLuminance → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageLuminance](https://www.vtk.org/doc/nightly/html/classvtkImageLuminance.html) converts RGB to a single-component grayscale image using perceptual luminance weights.
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) reads the `Gourds.png` color image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
