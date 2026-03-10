### Description

This example mirrors a 3D medical volume along the X axis using vtkImageFlip and displays the original and flipped slices side by side. The FullHead dataset is flipped left-to-right, demonstrating spatial transformation of image data. It follows the VTK pipeline structure:

**Reader → ImageFlip → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the original and flipped slices. `SetDisplayExtent()` selects the middle axial slice from each volume.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts the signed short data to unsigned char for display.
- [vtkImageFlip](https://www.vtk.org/doc/nightly/html/classvtkImageFlip.html) mirrors the volume along a specified axis. `SetFilteredAxis(0)` flips along the X axis (left-right). Use `1` for Y (top-bottom) or `2` for Z (front-back).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume (256×256×94 voxels of signed short scalars).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout showing original vs. flipped.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
