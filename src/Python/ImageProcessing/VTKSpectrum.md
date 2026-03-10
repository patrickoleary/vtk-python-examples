### Description

This example computes and displays the power spectrum of an image using the discrete Fourier transform. The left viewport shows the original image; the right shows the log-scaled, centered magnitude spectrum. The logarithmic transfer function compresses the large dynamic range of the spectrum for display. It follows the VTK pipeline structure:

**Reader → ImageFFT → ImageMagnitude → ImageFourierCenter → ImageLogarithmicScale → ImageMapToColors → ImageActor (right)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageFFT](https://www.vtk.org/doc/nightly/html/classvtkImageFFT.html) transforms the image to the frequency domain.
- [vtkImageFourierCenter](https://www.vtk.org/doc/nightly/html/classvtkImageFourierCenter.html) shifts the zero-frequency component to the center of the spectrum.
- [vtkImageLogarithmicScale](https://www.vtk.org/doc/nightly/html/classvtkImageLogarithmicScale.html) applies logarithmic scaling to compress the dynamic range.
- [vtkImageMagnitude](https://www.vtk.org/doc/nightly/html/classvtkImageMagnitude.html) computes the magnitude of the complex FFT output.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) maps scalar values to colors through a lookup table.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNMReader](https://www.vtk.org/doc/nightly/html/classvtkPNMReader.html) reads the `vtks.pgm` PGM image.
- [vtkWindowLevelLookupTable](https://www.vtk.org/doc/nightly/html/classvtkWindowLevelLookupTable.html) and [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) map spectrum values to displayable colors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
