### Description

This example computes the cross-correlation of an image with a small template using vtkImageCorrelation and displays the result side by side. The left viewport shows the original 128×128 image containing a bright white square on black. The right viewport shows the normalized correlation map — a fuzzy bright region appears where the 21×21 template best overlaps the image, fading to dark where there is little match. The bright region is shifted relative to the original square because the template is anchored at its corner (not its center), so the correlation peak is offset by approximately half the template size. The correlation values are normalized to [0, 255] for display. It follows the VTK pipeline structure:

**ImageCanvasSource2D (image) → ImageCast → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates the input image (128×128) and template (21×21).
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts image scalar type for display.
- [vtkImageCorrelation](https://www.vtk.org/doc/nightly/html/classvtkImageCorrelation.html) computes the cross-correlation of two images. `SetDimensionality(2)` performs the 2D correlation. The output values are sums of products and can be very large.
- [vtkImageShiftScale](https://www.vtk.org/doc/nightly/html/classvtkImageShiftScale.html) normalizes the correlation range to [0, 255] for visible display.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
