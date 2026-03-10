### Description

This example computes the full gradient vector of a medical volume slice using vtkImageGradient, then computes the gradient magnitude using vtkImageMagnitude. The left viewport shows the original CT head slice; the right shows the gradient magnitude — bright edges outline the skull, tissue boundaries, and internal structures on a dark background. Unlike vtkImageGradientMagnitude which computes only the scalar magnitude, vtkImageGradient produces a multi-component vector output. It follows the VTK pipeline structure:

**MetaImageReader → ImageCast → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D image slices.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts image scalar type for display.
- [vtkImageGradient](https://www.vtk.org/doc/nightly/html/classvtkImageGradient.html) computes the gradient vector (dx, dy) at each voxel. `SetDimensionality(2)` computes the 2D gradient. The output has two components.
- [vtkImageMagnitude](https://www.vtk.org/doc/nightly/html/classvtkImageMagnitude.html) computes the magnitude of the multi-component gradient vector.
- [vtkImageShiftScale](https://www.vtk.org/doc/nightly/html/classvtkImageShiftScale.html) normalizes the gradient magnitude to [0, 255] for visible display.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
