### Description

This example reads a NIfTI neuroimaging volume (.nii) using vtkNIFTIImageReader and display an axial slice with grayscale coloring. A small synthetic sinusoidal NIfTI volume is generated if the file does not already exist.

**Reader → LookupTable → ImageMapToColors → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a 2D image slice.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) maps scalars through a lookup table.
- [vtkImageSinusoidSource](https://www.vtk.org/doc/nightly/html/classvtkImageSinusoidSource.html) generates a procedural sinusoidal image.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to grayscale colors.
- [vtkNIFTIImageReader](https://www.vtk.org/doc/nightly/html/classvtkNIFTIImageReader.html) reads NIfTI-1 and NIfTI-2 image files used in neuroimaging.
- [vtkNIFTIImageWriter](https://www.vtk.org/doc/nightly/html/classvtkNIFTIImageWriter.html) writes NIfTI files (used to generate sample data).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
