### Description

This example applies a Butterworth low-pass filter in the frequency domain to smooth a 3D medical volume (FullHead.mhd). The left viewport shows the original middle axial slice of a CT head scan; the right shows the smoothed result where fine detail and noise are reduced while the overall structure of the skull and soft tissue is preserved. Compared to the original, the smoothed slice appears slightly blurred — edges are softer and small features are attenuated. It follows the VTK pipeline structure:

**Reader → ImageFFT → ButterworthLowPass → ImageRFFT → ExtractComponents → ImageShiftScale → ImageActor (right)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageButterworthLowPass](https://www.vtk.org/doc/nightly/html/classvtkImageButterworthLowPass.html) attenuates high frequencies. `SetCutOff()` defines the cutoff frequency and `SetOrder()` controls the roll-off steepness.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts image scalar type for display.
- [vtkImageExtractComponents](https://www.vtk.org/doc/nightly/html/classvtkImageExtractComponents.html) extracts the real component from the complex output.
- [vtkImageFFT](https://www.vtk.org/doc/nightly/html/classvtkImageFFT.html) transforms the image to the frequency domain. `SetDimensionality(2)` performs a 2D FFT per slice.
- [vtkImageRFFT](https://www.vtk.org/doc/nightly/html/classvtkImageRFFT.html) performs the inverse FFT to return to the spatial domain.
- [vtkImageShiftScale](https://www.vtk.org/doc/nightly/html/classvtkImageShiftScale.html) maps the filtered output to unsigned char for display.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
