### Description

This example applies a Butterworth high-pass filter in the frequency domain to enhance edges in a medical volume slice and displays the original and filtered images side by side. The left viewport shows the original CT head scan slice; the right shows the high-pass result where only edges and fine detail remain — skull boundaries and tissue interfaces appear as bright outlines on a dark background. Unlike the ideal high-pass filter, the Butterworth filter provides a smooth rolloff that reduces ringing artifacts. It follows the VTK pipeline structure:

**MetaImageReader → ImageCast → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D image slices.
- [vtkImageButterworthHighPass](https://www.vtk.org/doc/nightly/html/classvtkImageButterworthHighPass.html) attenuates low frequencies with a smooth rolloff. `SetXCutOff()` and `SetYCutOff()` set the cutoff frequencies. `SetOrder()` controls the rolloff steepness.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts to unsigned char for display.
- [vtkImageFFT](https://www.vtk.org/doc/nightly/html/classvtkImageFFT.html) transforms the image to the frequency domain.
- [vtkImageMagnitude](https://www.vtk.org/doc/nightly/html/classvtkImageMagnitude.html) extracts real magnitude from the complex output.
- [vtkImageRFFT](https://www.vtk.org/doc/nightly/html/classvtkImageRFFT.html) transforms back to the spatial domain.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
