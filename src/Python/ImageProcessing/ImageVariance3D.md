### Description

This example computes the local variance of a medical volume slice using vtkImageVariance3D and displays the original and variance images side by side. High variance indicates regions with rapid intensity changes such as edges and boundaries. It follows the VTK pipeline structure:

**MetaImageReader → ImageCast → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D image slices.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts to unsigned char for display.
- [vtkImageVariance3D](https://www.vtk.org/doc/nightly/html/classvtkImageVariance3D.html) computes the local variance in a 5×5×1 neighborhood. `SetKernelSize()` controls the neighborhood dimensions.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
