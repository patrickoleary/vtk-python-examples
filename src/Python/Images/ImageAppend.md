### Description

This example combines three separate grayscale images into a single RGB image using vtkImageAppendComponents. Each single-component canvas provides one color channel (R, G, B), and the result is displayed as a composite color image. It follows the VTK pipeline structure:

**ImageCanvasSource2D (R) → ImageAppendComponents → ImageActor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the 2D image.
- [vtkImageAppendComponents](https://www.vtk.org/doc/nightly/html/classvtkImageAppendComponents.html) combines multiple single-component images into a single multi-component image. Three inputs produce an RGB image.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates three 128×128 single-component canvases representing the R, G, and B channels.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with `ParallelProjectionOn()` for correct 2D viewing.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
