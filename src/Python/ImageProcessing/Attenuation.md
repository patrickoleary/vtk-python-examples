### Description

This example thises MRI image illustrates attenuation that can occur due to sensor position. The artifact is removed by multiplying by an attenuation profile determined manually using vtkSphere and vtkSampleFunction. The left viewport shows the original image; the right shows the corrected result. It follows the VTK pipeline structure:

**Reader → ImageCast → GaussianSmooth → ImageMathematics (Multiply) → ImageActor (right)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to double for arithmetic operations.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) smooths the image to reduce discrete scalar artifacts.
- [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) multiplies the smoothed image with the attenuation profile to correct the artifact.
- [vtkImageShiftScale](https://www.vtk.org/doc/nightly/html/classvtkImageShiftScale.html) scales the distance field to match the attenuation profile.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNMReader](https://www.vtk.org/doc/nightly/html/classvtkPNMReader.html) reads the `AttenuationArtifact.pgm` PGM image.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) samples an implicit function over a grid.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) and [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) generate a distance field modeling the sensor sensitivity fall-off.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
