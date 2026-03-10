### Description

This example displays a medical volume slice using radiology-style window/level grayscale mapping via vtkImageMapToWindowLevelColors. The window parameter controls the contrast range and the level parameter controls the brightness center. It follows the VTK pipeline structure:

**MetaImageReader → ImageMapToWindowLevelColors → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a 2D slice of the volume. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageMapToWindowLevelColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToWindowLevelColors.html) maps scalar values to grayscale using window (contrast range) and level (brightness center) settings.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with `ParallelProjectionOn()` for correct 2D viewing.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
