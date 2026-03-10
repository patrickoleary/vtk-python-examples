### Description

This example swaps axes of a 3D medical volume (FullHead.mhd) using vtkImagePermute to convert an axial view to a coronal view. The left viewport shows the original middle axial slice; the right shows the middle coronal slice after permuting axes. It follows the VTK pipeline structure:

**Reader → ImagePermute → ImageCast → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle slice.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display.
- [vtkImagePermute](https://www.vtk.org/doc/nightly/html/classvtkImagePermute.html) reorders the volume axes. `SetFilteredAxes(0, 2, 1)` swaps Y and Z, converting axial slices to coronal slices.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
