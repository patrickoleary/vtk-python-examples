### Description

This example displays an oblique reslice of a CT head volume. The reslice plane is tilted 30 degrees about the X axis through the volume center, rendered with the standard vtkImageActor pipeline.

**Reader → ImageReslice → ImageMapToColors (LookupTable) → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the resliced image on a quadrilateral plane.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) maps resliced scalars to grayscale colors.
- [vtkImageReslice](https://www.vtk.org/doc/nightly/html/classvtkImageReslice.html) extracts an oblique 2D slice defined by direction cosines and origin.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) defines a grayscale scalar-to-color mapping.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the MetaImage (.mhd/.raw) CT volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
