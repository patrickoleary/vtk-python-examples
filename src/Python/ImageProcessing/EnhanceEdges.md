### Description

This example demonstrates edge enhancement by subtracting the Laplacian from the original image. Three viewports show the original (left), the Laplacian (center), and the enhanced result (right) for a slice of the FullHead volume. The Laplacian is a second-derivative high-pass filter that isolates edges; subtracting it from the original sharpens the image. It follows the VTK pipeline structure:

**Reader → ImageCast → ImageLaplacian → ImageMapToWindowLevelColors → ImageActor (center)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a 2D image slice on a quadrilateral plane.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts image scalar type for display.
- [vtkImageLaplacian](https://www.vtk.org/doc/nightly/html/classvtkImageLaplacian.html) second-derivative edge detection.
- [vtkImageMapToWindowLevelColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToWindowLevelColors.html) original slice (left viewport).
- [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) performs pixel-wise arithmetic on images.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads a MetaImage (.mhd/.raw) volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
