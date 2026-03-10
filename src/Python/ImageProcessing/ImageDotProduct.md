### Description

This example computes the dot product of two multi-component images using vtkImageDotProduct and displays the inputs and result in a 3-viewport layout. The left viewport shows a wide horizontal yellow bar (R=255, G=255); the center shows a tall vertical cyan bar (G=255, B=255). The right viewport shows the dot product — a bright white square appears only where the two bars cross, since the shared green channel produces a non-zero dot product (255×255) at the intersection. Everywhere else is black because at least one of the two images is zero at that pixel. It follows the VTK pipeline structure:

**ImageCanvasSource2D → ImageCast → ImageActor (left, horizontal yellow bar)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates two 256×256 RGB images — one with a horizontal yellow bar, one with a vertical cyan bar that crosses it.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts image scalar type for display.
- [vtkImageDotProduct](https://www.vtk.org/doc/nightly/html/classvtkImageDotProduct.html) computes the per-pixel dot product of the two multi-component images. The output is a single-component scalar image. Values can be very large (sums of component products).
- [vtkImageShiftScale](https://www.vtk.org/doc/nightly/html/classvtkImageShiftScale.html) normalizes the dot product range to [0, 255] for visible display.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — three renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
