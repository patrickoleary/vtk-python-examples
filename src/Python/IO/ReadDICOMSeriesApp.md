### Description

This example reads a directory of DICOM files and allows interactive browsing through slices using the mouse wheel or Up/Down keys, with a slice counter overlay.

**Reader → Actor → Custom InteractorStyle → Renderer → Window → Interactor**

- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) renders 2D overlay geometry.
- [vtkDICOMImageReader](https://www.vtk.org/doc/nightly/html/classvtkDICOMImageReader.html) reads all DICOM files from a directory into a 3D volume. `SetDirectoryName()` specifies the folder containing the DICOM series.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a single slice as a 2D texture. `SetDisplayExtent()` selects the visible Z slice. `GetProperty().SetColorWindow()` and `SetColorLevel()` map the scalar range to grayscale.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D image-appropriate interaction (pan and zoom).
- [vtkTextMapper](https://www.vtk.org/doc/nightly/html/classvtkTextMapper.html) and [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) create text overlays showing the current slice number and usage hints.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) defines text appearance (font, color, size).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().ParallelProjectionOn()` ensures the image is displayed without perspective distortion. `ResetCamera()` is called after each slice change to keep the camera centered.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
