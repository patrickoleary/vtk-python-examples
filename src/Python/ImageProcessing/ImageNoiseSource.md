### Description

This example generates and displays a random noise image using vtkImageNoiseSource. The noise image is a 256×256 2D image with uniformly distributed random values mapped to grayscale. No external data files are needed. It follows the VTK pipeline structure:

**ImageNoiseSource → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the 2D noise image.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display.
- [vtkImageNoiseSource](https://www.vtk.org/doc/nightly/html/classvtkImageNoiseSource.html) generates a synthetic image with random noise. `SetWholeExtent()` defines the image dimensions. `SetMinimum()` and `SetMaximum()` control the value range.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a black background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
