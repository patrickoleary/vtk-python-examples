### Description

This example alpha-blends two images using vtkImageBlend. The original FullHead slice is blended with a Sobel edge-detected version to create a composite that highlights edges over the anatomy. Three viewports show the original, the edges, and the blended result. It follows the VTK pipeline structure:

**Reader → ImageCast → ImageActor (left)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageBlend](https://www.vtk.org/doc/nightly/html/classvtkImageBlend.html) alpha-blends two images. `SetOpacity(0, 0.6)` and `SetOpacity(1, 0.4)` control the contribution of each input. Unlike vtkImageWeightedSum, vtkImageBlend supports per-input opacity and alpha channels.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display.
- [vtkImageMagnitude](https://www.vtk.org/doc/nightly/html/classvtkImageMagnitude.html) computes the magnitude of the gradient vector.
- [vtkImageSobel2D](https://www.vtk.org/doc/nightly/html/classvtkImageSobel2D.html) computes the Sobel gradient for edge detection.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — three renderers with `SetViewport()` create a three-panel layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
