### Description

This example computes the city-block (Manhattan) distance transform of a binary image using vtkImageCityBlockDistance and displays the original and distance map side by side. The left viewport shows the original binary image (white shapes on black); the right shows the distance map where each pixel's brightness indicates its Manhattan distance to the nearest zero-valued (black) pixel — white regions glow brightest at their centers and fade toward their edges. It follows the VTK pipeline structure:

**PNMReader → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts to short — `vtkImageCityBlockDistance` requires short scalar input.
- [vtkImageCityBlockDistance](https://www.vtk.org/doc/nightly/html/classvtkImageCityBlockDistance.html) computes the city-block distance transform. `SetDimensionality(2)` computes the 2D distance.
- [vtkImageShiftScale](https://www.vtk.org/doc/nightly/html/classvtkImageShiftScale.html) normalizes the distance values to [0, 255] for visible display.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNMReader](https://www.vtk.org/doc/nightly/html/classvtkPNMReader.html) reads the `binary.pgm` binary image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
