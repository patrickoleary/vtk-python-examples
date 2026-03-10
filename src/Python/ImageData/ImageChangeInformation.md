### Description

This example modifies the spacing and origin of a procedural image using [vtkImageChangeInformation](https://www.vtk.org/doc/nightly/html/classvtkImageChangeInformation.html) and display the original and modified images side by side. The pixel data is identical in both viewports — only the metadata that maps the image to world coordinates is changed.

**ImageCanvasSource2D → ImageChangeInformation → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a procedural canvas with a colored box.
- [vtkImageChangeInformation](https://www.vtk.org/doc/nightly/html/classvtkImageChangeInformation.html) modifies image metadata (spacing, origin, extent) without altering pixel data.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays text labels showing spacing and origin values.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene; two renderers create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
