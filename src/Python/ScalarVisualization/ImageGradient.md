### Description

This example visualizes gradient information of a CT head slice as an HSV color image.

**Reader → Cast → Magnify → Smooth → Gradient → EuclideanToPolar → Pad → ExtractComponents → HSVToRGB → Cast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the image slice.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) casts scalar types for processing and display.
- [vtkImageConstantPad](https://www.vtk.org/doc/nightly/html/classvtkImageConstantPad.html) adds a third component for HSV representation.
- [vtkImageEuclideanToPolar](https://www.vtk.org/doc/nightly/html/classvtkImageEuclideanToPolar.html) converts gradient to polar coordinates.
- [vtkImageExtractComponents](https://www.vtk.org/doc/nightly/html/classvtkImageExtractComponents.html) permutes components into HSV order.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) smooths the image to remove artifacts.
- [vtkImageGradient](https://www.vtk.org/doc/nightly/html/classvtkImageGradient.html) computes the 2D gradient.
- [vtkImageHSVToRGB](https://www.vtk.org/doc/nightly/html/classvtkImageHSVToRGB.html) converts HSV to RGB for display.
- [vtkImageMagnify](https://www.vtk.org/doc/nightly/html/classvtkImageMagnify.html) magnifies the image with interpolation.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the CT head volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
