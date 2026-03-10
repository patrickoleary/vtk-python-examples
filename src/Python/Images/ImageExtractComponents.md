### Description

This example extracts individual R, G, B channels from a color JPEG image and displays them in a 2×2 grid alongside the original using vtkImageExtractComponents. Top-left shows the original color image; top-right the red channel; bottom-left the green channel; bottom-right the blue channel. It follows the VTK pipeline structure:

**JpegReader → ImageActor (top-left)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageExtractComponents](https://www.vtk.org/doc/nightly/html/classvtkImageExtractComponents.html) extracts a single scalar component (R=0, G=1, B=2) from the multi-component image.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkJPEGReader](https://www.vtk.org/doc/nightly/html/classvtkJPEGReader.html) reads the `Gourds2.jpg` color image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — four renderers with `SetViewport()` create a 2×2 grid layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
