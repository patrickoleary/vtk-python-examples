### Description

This example reslices a 3D medical volume along an oblique plane using vtkImageReslice and displays the result as a 2D image. The FullHead dataset is sliced at a 25-degree tilt around the Y axis through the center of the volume. It follows the VTK pipeline structure:

**Reader → ImageReslice → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the resliced 2D image in the 3D scene.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts the signed short output to unsigned char for display. `ClampOverflowOn()` prevents wrap-around artifacts.
- [vtkImageReslice](https://www.vtk.org/doc/nightly/html/classvtkImageReslice.html) extracts an arbitrary 2D slice from the 3D volume. `SetResliceAxesDirectionCosines()` defines the oblique cutting plane orientation. `SetResliceAxesOrigin()` positions the slice through the center of the volume. `SetInterpolationModeToLinear()` smooths the resampled output.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume (256×256×94 voxels of signed short scalars).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a black background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
