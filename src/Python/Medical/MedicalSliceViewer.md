### Description

This example displays a 2D axial slice from a CT head volume using the standard vtkImageActor rendering pipeline. A grayscale lookup table maps CT intensity values to display colors. The middle slice along the Z axis is shown.

**Reader → ImageMapToColors (LookupTable) → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a 2D image slice on a quadrilateral plane.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) maps CT intensity scalars to grayscale colors.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) defines a grayscale scalar-to-color mapping.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the MetaImage (.mhd/.raw) CT volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
