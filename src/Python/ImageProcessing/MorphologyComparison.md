### Description

This example demonstrates various binary morphological filters that can alter the shape of segmented regions. Six viewports (2×3 grid) show: original, connectivity, erosion, dilation, opening, and closing. Erosion shrinks regions, dilation grows them, opening (dilate then erode) removes small islands, closing (erode then dilate) fills small holes, and connectivity extracts a connected component from a seed point. It follows the VTK pipeline structure:

**Reader → ImageDilateErode3D / ImageSeedConnectivity → ImageActor (per viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D images with nearest-neighbor interpolation.
- [vtkImageDilateErode3D](https://www.vtk.org/doc/nightly/html/classvtkImageDilateErode3D.html) performs dilation and erosion with a 31×31 kernel. Chaining two instances creates opening or closing operations.
- [vtkImageSeedConnectivity](https://www.vtk.org/doc/nightly/html/classvtkImageSeedConnectivity.html) extracts the connected region touching a seed point.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkPNMReader](https://www.vtk.org/doc/nightly/html/classvtkPNMReader.html) reads the `binary.pgm` binary image.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — six renderers with `SetViewport()` create a 2×3 grid layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
