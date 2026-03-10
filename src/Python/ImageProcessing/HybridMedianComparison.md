### Description

This example compares median and hybrid-median filters for removing shot noise from a test pattern image. Four viewports show the original (top-left), noisy (top-right), hybrid median (bottom-left), and standard median (bottom-right). The hybrid filter preserves corners and thin lines better than the standard median filter. It follows the VTK pipeline structure:

**Reader → ImageCast → (add shot noise) → ImageHybridMedian2D (×2) → ImageActor (bottom-left)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images with window/level settings.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to double for arithmetic.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) represents a regular image or volume.
- [vtkImageHybridMedian2D](https://www.vtk.org/doc/nightly/html/classvtkImageHybridMedian2D.html) applies a hybrid median filter that uses cross and X-shaped neighborhoods to preserve corners and thin lines.
- [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) performs pixel-wise arithmetic on images.
- [vtkImageMedian3D](https://www.vtk.org/doc/nightly/html/classvtkImageMedian3D.html) applies a standard median filter with a 5×5 kernel.
- [vtkImageNoiseSource](https://www.vtk.org/doc/nightly/html/classvtkImageNoiseSource.html), [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html), and [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) generate and add shot noise to the image.
- [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html) segments image data by scalar range.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) reads the `TestPattern.png` image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — four renderers with `SetViewport()` create a 2×2 grid layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
