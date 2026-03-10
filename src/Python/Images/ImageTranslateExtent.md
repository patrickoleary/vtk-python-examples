### Description

This example shifts the extent of an image using vtkImageTranslateExtent and displays the original and translated images side by side with text labels showing the extent values. The pixel data is identical in both viewports — `vtkImageTranslateExtent` does not modify any pixels. It only changes the extent metadata that describes where the image sits in world coordinates. The left viewport shows the original extent `[0, 99] × [0, 99]`; the right shows the translated extent `[60, 159] × [40, 139]`. This metadata shift matters when compositing multiple images or aligning an image with other spatial data. It follows the VTK pipeline structure:

**ImageCanvasSource2D → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a 100×100 RGB canvas with an orange box.
- [vtkImageTranslateExtent](https://www.vtk.org/doc/nightly/html/classvtkImageTranslateExtent.html) shifts the image extent in world coordinates without modifying pixel data. `SetTranslation(60, 40, 0)` offsets the extent by +60 in X and +40 in Y.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays white text labels in each viewport showing the extent values so the metadata change is visible.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
