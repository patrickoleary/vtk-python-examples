### Description

This example computes the local range (max − min) of a medical volume slice using vtkImageRange3D and displays the original and range images side by side. High range values indicate regions with large intensity variation such as edges. It follows the VTK pipeline structure:

**MetaImageReader → ImageCast → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D image slices.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts to unsigned char for display.
- [vtkImageRange3D](https://www.vtk.org/doc/nightly/html/classvtkImageRange3D.html) computes the local range in a 5×5×1 neighborhood. `SetKernelSize()` controls the neighborhood dimensions.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
