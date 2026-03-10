### Description

This example applies an ideal low-pass filter in the frequency domain to smooth a medical volume slice and displays the original and filtered images side by side. The ideal low-pass filter zeros all frequencies above a cutoff, producing a smoothed image (with ringing artifacts typical of ideal filters). It follows the VTK pipeline structure:

**MetaImageReader → ImageCast → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D image slices.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts to unsigned char for display.
- [vtkImageFFT](https://www.vtk.org/doc/nightly/html/classvtkImageFFT.html) transforms the image to the frequency domain.
- [vtkImageIdealLowPass](https://www.vtk.org/doc/nightly/html/classvtkImageIdealLowPass.html) zeros all frequencies above the cutoff values. `SetXCutOff()` and `SetYCutOff()` set the cutoff in each dimension.
- [vtkImageMagnitude](https://www.vtk.org/doc/nightly/html/classvtkImageMagnitude.html) extracts real magnitude from the complex output.
- [vtkImageRFFT](https://www.vtk.org/doc/nightly/html/classvtkImageRFFT.html) transforms back to the spatial domain.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
