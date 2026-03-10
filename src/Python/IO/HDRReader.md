### Description

This example reads an HDR (high-dynamic-range) image file and displays it using the standard VTK pipeline with parallel projection and 2D image interaction.

**Reader → Actor → Renderer → Window → Interactor**

- [vtkHDRReader](https://www.vtk.org/doc/nightly/html/classvtkHDRReader.html) reads a Radiance HDR (.hdr) image file. `SetFileName()` specifies the input file. HDR images store floating-point color values, enabling a wider luminance range than standard 8-bit formats.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the image as a 2D texture. `GetProperty().SetColorWindow()` and `SetColorLevel()` control the mapping from HDR values to the displayable range.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D pan and zoom interaction suitable for image viewing.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().ParallelProjectionOn()` ensures the image is displayed without perspective distortion.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
