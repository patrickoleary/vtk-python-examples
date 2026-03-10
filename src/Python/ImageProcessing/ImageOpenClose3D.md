### Description

This example applies morphological opening and closing to a procedural binary image using vtkImageOpenClose3D and displays the original, opened, and closed images in a 3-viewport layout. The left viewport shows the original — a large rectangle with small dark holes, small isolated bright dots, and two blocks connected by thin bridges. The center shows the opened result (erode then dilate) — the small bright dots disappear, thin bridges break, and large shapes are slightly rounded. The right shows the closed result (dilate then erode) — the small dark holes in the rectangle are filled in, and shapes are slightly expanded. A 9×9 kernel is used so the effects are dramatic. It follows the VTK pipeline structure:

**ImageCanvasSource2D → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a 256×256 binary canvas with small holes, small dots, and thin bridges to demonstrate morphological effects.
- [vtkImageOpenClose3D](https://www.vtk.org/doc/nightly/html/classvtkImageOpenClose3D.html) performs morphological opening or closing. `SetKernelSize()` controls the structuring element. `SetOpenValue()` and `SetCloseValue()` configure the operation direction.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — three renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
