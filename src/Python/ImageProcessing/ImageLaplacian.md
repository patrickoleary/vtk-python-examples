### Description

This example applies a Laplacian filter to a 3D medical volume (FullHead.mhd) for second-derivative edge detection. The left viewport shows the original middle axial slice; the right shows the Laplacian result. The Laplacian highlights regions of rapid intensity change — edges appear as bright or dark lines against a neutral background. It follows the VTK pipeline structure:

**Reader → ImageLaplacian → ImageCast → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display.
- [vtkImageLaplacian](https://www.vtk.org/doc/nightly/html/classvtkImageLaplacian.html) computes the discrete Laplacian (sum of second partial derivatives). `SetDimensionality(2)` restricts computation to the XY plane.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
