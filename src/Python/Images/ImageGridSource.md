### Description

This example generates and displays a grid pattern image using vtkImageGridSource. The source produces a 256×256 unsigned char image with white grid lines on a black background. It follows the VTK pipeline structure:

**ImageGridSource → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the 2D image.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts image scalar type for display.
- [vtkImageGridSource](https://www.vtk.org/doc/nightly/html/classvtkImageGridSource.html) generates a procedural grid pattern image. `SetGridSpacing()` controls the distance between grid lines, `SetLineValue()` and `SetFillValue()` control the line and background intensities.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with `ParallelProjectionOn()` for correct 2D viewing.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
