### Description

This example extracts a connected region from a binary image using vtkImageSeedConnectivity. The left viewport shows the full binary input — six disconnected white rectangles on a black background. The right viewport shows only the single rectangle connected to the seed point at (30, 30) — all other shapes are removed. This demonstrates seed-based flood-fill connectivity extraction. It follows the VTK pipeline structure:

**ImageCanvasSource2D → ImageActor (left, all shapes)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a 256×256 binary canvas with six disconnected white rectangles.
- [vtkImageSeedConnectivity](https://www.vtk.org/doc/nightly/html/classvtkImageSeedConnectivity.html) performs seed-based flood fill. `AddSeed()` specifies the starting pixel. `SetInputConnectValue()` defines which pixel value to flood through. Only the region connected to the seed is kept; all other pixels are set to `OutputUnconnectedValue`.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
