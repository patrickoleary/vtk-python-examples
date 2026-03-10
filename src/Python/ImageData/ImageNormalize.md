### Description

This example normalizes an RGB image so that each pixel's color vector has unit magnitude using vtkImageNormalize. The left viewport shows the original image with four colored rectangles of varying brightness; the right shows the normalized result where all regions appear at similar brightness but the color direction (hue) is preserved. For example, a dim dark-red block and a bright red block both become the same saturated red after normalization. It follows the VTK pipeline structure:

**ImageCanvasSource2D → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a 256×256 RGB canvas with four colored rectangles at different brightness levels.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts to float before normalization so fractional results are preserved, then back to unsigned char for display.
- [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) scales the normalized [0..1] components back to [0..255] for unsigned char display.
- [vtkImageNormalize](https://www.vtk.org/doc/nightly/html/classvtkImageNormalize.html) scales each pixel's RGB vector to unit magnitude. This equalizes brightness across all pixels while preserving their color direction.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
