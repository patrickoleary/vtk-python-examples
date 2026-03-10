### Description

This example resamples a 3D medical volume (FullHead.mhd) to a different resolution using vtkImageResize. The left viewport shows the original middle axial slice; the right shows the resized (downsampled to half resolution) version. It follows the VTK pipeline structure:

**Reader → ImageResize → ImageCast → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display.
- [vtkImageResize](https://www.vtk.org/doc/nightly/html/classvtkImageResize.html) resamples the image. `SetResizeMethodToMagnificationFactors()` and `SetMagnificationFactors(0.5, 0.5, 1.0)` downsample X and Y by half while keeping Z unchanged.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
