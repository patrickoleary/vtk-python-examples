### Description

This example applies a Sobel 2D edge detector to a slice of a 3D medical volume (FullHead.mhd). The left viewport shows the original middle axial slice; the right shows the Sobel edge-detected result. vtkImageSobel2D produces a 2-component gradient output which is converted to a single scalar using vtkImageMagnitude. It follows the VTK pipeline structure:

**Reader → ImageSobel2D → ImageMagnitude → ImageCast → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display.
- [vtkImageExtractComponents](https://www.vtk.org/doc/nightly/html/classvtkImageExtractComponents.html) provides image extract components functionality.
- [vtkImageMagnitude](https://www.vtk.org/doc/nightly/html/classvtkImageMagnitude.html) computes the magnitude of the 2-component gradient vector, yielding a single scalar edge strength.
- [vtkImageSobel2D](https://www.vtk.org/doc/nightly/html/classvtkImageSobel2D.html) computes the Sobel gradient in X and Y, producing a 2-component output.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
