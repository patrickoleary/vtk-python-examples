### Description

This example compares constant padding and mirror padding for reducing border artifacts during frequency-domain processing. The discrete Fourier transform treats the image as periodic, so pixels on opposite borders are adjacent. This can distort the frequency spectrum. Padding the image before processing eliminates these wraparound artifacts. The left viewport shows constant-value padding (800); the right shows mirror padding. It follows the VTK pipeline structure:

**Reader → ImageConstantPad → ImageMapToWindowLevelColors → ImageActor (left)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageConstantPad](https://www.vtk.org/doc/nightly/html/classvtkImageConstantPad.html) pads the image with a constant scalar value.
- [vtkImageMapToWindowLevelColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToWindowLevelColors.html) maps scalar values to grayscale via window/level settings.
- [vtkImageMirrorPad](https://www.vtk.org/doc/nightly/html/classvtkImageMirrorPad.html) pads the image by reflecting pixels at the borders, producing a continuous periodic extension.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
