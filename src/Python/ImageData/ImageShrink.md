### Description

This example downsamples a 3D medical volume (FullHead.mhd) by an integer factor using vtkImageShrink3D. The left viewport shows the original middle axial slice; the right shows the downsampled version. `AveragingOn()` applies a box filter before subsampling to reduce aliasing. It follows the VTK pipeline structure:

**Reader → ImageShrink3D → ImageCast → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display.
- [vtkImageShrink3D](https://www.vtk.org/doc/nightly/html/classvtkImageShrink3D.html) downsamples the image by integer factors. `SetShrinkFactors(4, 4, 1)` reduces X and Y by 4× while keeping Z unchanged. `AveragingOn()` applies a mean filter before subsampling.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
