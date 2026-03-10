### Description

This example compares Gaussian and median smoothing for reducing low-probability high-amplitude (shot) noise on a slice of FullHead.mhd. Four viewports show the original (top-left), noisy (top-right), Gaussian smoothed (bottom-left), and median filtered (bottom-right). The median filter preserves edges better than Gaussian smoothing. It follows the VTK pipeline structure:

**Reader → ImageCast → (add shot noise) → ImageGaussianSmooth → ImageActor (bottom-left)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices with window/level settings.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to double for arithmetic.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) represents a regular image or volume.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) applies a Gaussian low-pass filter that blurs edges along with noise.
- [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) performs pixel-wise arithmetic on images.
- [vtkImageMedian3D](https://www.vtk.org/doc/nightly/html/classvtkImageMedian3D.html) applies a 5×5 median filter that removes shot noise while preserving edges.
- [vtkImageNoiseSource](https://www.vtk.org/doc/nightly/html/classvtkImageNoiseSource.html), [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html), and [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) generate and add shot noise.
- [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html) segments image data by scalar range.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — four renderers with `SetViewport()` create a 2×2 grid layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
