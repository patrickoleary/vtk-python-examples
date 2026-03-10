### Description

This example applies boolean logic operations (AND, OR, XOR) to two binary images using vtkImageLogic. A circle and a rectangle are created procedurally with vtkImageCanvasSource2D and combined with each operation. The five-viewport layout shows Source 1 (circle), Source 2 (rectangle), AND (intersection), OR (union), and XOR (symmetric difference). It follows the VTK pipeline structure:

**CanvasSource → ImageLogic → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images. Five actors show the two sources and three logic results.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates procedural binary images. `DrawCircle()` draws a filled circle and `FillBox()` draws a filled rectangle.
- [vtkImageLogic](https://www.vtk.org/doc/nightly/html/classvtkImageLogic.html) performs pixel-wise boolean operations on two binary images. `SetOperationToAnd()`, `SetOperationToOr()`, and `SetOperationToXor()` select the logic function. `SetOutputTrueValue(255)` sets the output value for true pixels.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — five renderers with `SetViewport()` create a side-by-side layout. Cameras are shared so all viewports pan and zoom together.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
