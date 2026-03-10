### Description

This example computes the gradient magnitude of a CT head volume and display a 2D axial slice showing tissue boundaries. The gradient magnitude highlights edges — regions of rapid intensity change — using the standard vtkImageActor rendering pipeline.

**Reader → ImageGradientMagnitude → ImageMapToColors (LookupTable) → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a 2D image slice on a quadrilateral plane.
- [vtkImageGradientMagnitude](https://www.vtk.org/doc/nightly/html/classvtkImageGradientMagnitude.html) computes edge strength in the XY plane.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) maps gradient scalars to grayscale colors.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) defines a grayscale scalar-to-color mapping.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the MetaImage (.mhd/.raw) CT volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
