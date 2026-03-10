### Description

This example displays the middle axial slice of a 3D medical volume (FullHead.mhd) using the standard VTK rendering pipeline with vtkImageActor, vtkImageCast, parallel projection, and vtkInteractorStyleImage for proper 2D slice viewing. It follows the VTK pipeline structure:

**Reader → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a 2D slice of the volume. `SetDisplayExtent()` selects the middle axial slice by fixing the Z range to a single value.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts the signed short data to unsigned char for display. `ClampOverflowOn()` prevents wrap-around artifacts.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction — pan and zoom without 3D rotation.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume (256×256×94 voxels of signed short scalars).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a black background. `ParallelProjectionOn()` eliminates perspective distortion for correct 2D viewing.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
