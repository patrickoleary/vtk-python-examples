### Description

This example compares ideal and Butterworth high-pass filters in the frequency domain. The left viewport shows the ideal high-pass result (with ringing due to the abrupt cutoff); the right shows the Butterworth result (gradual attenuation, less ringing). The Butterworth filter attenuates frequencies with the function `out(i,j) = 1 / (1 + pow(CutOff/Freq(i,j), 2*Order))`. It follows the VTK pipeline structure:

**Reader → FFT → IdealHighPass → RFFT → ExtractComponents → WindowLevelColors → ImageActor (left)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageButterworthHighPass](https://www.vtk.org/doc/nightly/html/classvtkImageButterworthHighPass.html) applies a gradual high-pass filter that avoids ringing.
- [vtkImageExtractComponents](https://www.vtk.org/doc/nightly/html/classvtkImageExtractComponents.html) extracts the real component from the complex output.
- [vtkImageFFT](https://www.vtk.org/doc/nightly/html/classvtkImageFFT.html) transforms the image to the frequency domain.
- [vtkImageIdealHighPass](https://www.vtk.org/doc/nightly/html/classvtkImageIdealHighPass.html) applies a sharp cutoff high-pass filter. The abrupt transition causes ringing artifacts.
- [vtkImageMapToWindowLevelColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToWindowLevelColors.html) maps scalar values to grayscale via window/level settings.
- [vtkImageRFFT](https://www.vtk.org/doc/nightly/html/classvtkImageRFFT.html) transforms back to the spatial domain.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) reads the `fullhead15.png` image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
