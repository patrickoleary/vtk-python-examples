### Description

This example applies morphological dilation and erosion to a binary image using vtkImageDilateErode3D and displays the original, dilated, and eroded images in a 3-viewport layout. The left viewport shows the original binary shapes. The center shows the dilated result — white regions are visibly thicker, expanded by about 4 pixels in every direction. The right shows the eroded result — white regions are visibly thinner, shrunk inward by the same amount. A 9×9 kernel is used so the effect is clearly visible. It follows the VTK pipeline structure:

**PNMReader → ImageActor (left, original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images.
- [vtkImageDilateErode3D](https://www.vtk.org/doc/nightly/html/classvtkImageDilateErode3D.html) performs morphological dilation or erosion with a flat structuring element. `SetKernelSize()` controls the neighborhood. `SetDilateValue()` and `SetErodeValue()` define which value expands and which shrinks.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNMReader](https://www.vtk.org/doc/nightly/html/classvtkPNMReader.html) reads the `binary.pgm` binary image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — three renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
