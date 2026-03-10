### Description

This example converts an RGB image to grayscale luminance, then applies a rainbow lookup table via vtkImageMapToColors to produce a vivid false-color image. The left viewport shows the original `Gourds2.jpg` color photograph; the right shows a rainbow false-color version where dark regions appear blue, mid-tones green/yellow, and bright regions red. It follows the VTK pipeline structure:

**JpegReader → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageExtractComponents](https://www.vtk.org/doc/nightly/html/classvtkImageExtractComponents.html) provides image extract components functionality.
- [vtkImageMagnitude](https://www.vtk.org/doc/nightly/html/classvtkImageMagnitude.html) computes per-pixel magnitude of the RGB components, producing a single-component grayscale luminance image.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) maps single-component scalar values through the lookup table to produce an RGB false-color image.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkJPEGReader](https://www.vtk.org/doc/nightly/html/classvtkJPEGReader.html) reads the `Gourds2.jpg` RGB image.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) defines a blue → cyan → green → yellow → red rainbow ramp with 256 entries. `SetRange()` maps it to the luminance data range.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
