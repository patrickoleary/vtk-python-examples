### Description

This example computes a weighted sum of two procedural images using vtkImageWeightedSum and displays the inputs alongside the result. A sinusoidal pattern and a canvas with geometric shapes are blended with weights 0.6 and 0.4. Three viewports show the inputs and the blended output. It follows the VTK pipeline structure:

**Source1 + Source2 → ImageWeightedSum → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays each 2D image in the scene. Three actors are used for the three viewports.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a canvas image with geometric shapes (a filled box and a circle) as the second input.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts each output to unsigned char for display.
- [vtkImageSinusoidSource](https://www.vtk.org/doc/nightly/html/classvtkImageSinusoidSource.html) generates a procedural sinusoidal image as the first input.
- [vtkImageWeightedSum](https://www.vtk.org/doc/nightly/html/classvtkImageWeightedSum.html) computes the weighted sum of multiple images. `AddInputConnection()` adds each image and `SetWeight()` assigns its contribution. The output is `w₀·image₀ + w₁·image₁`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — three renderers with `SetViewport()` create a left/center/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
