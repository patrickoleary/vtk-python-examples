### Description

This example reads a single DICOM image file and displays it using the standard VTK pipeline with parallel projection and 2D image interaction.

**Reader → Actor → Renderer → Window → Interactor**

- [vtkDICOMImageReader](https://www.vtk.org/doc/nightly/html/classvtkDICOMImageReader.html) reads a single DICOM image file. `SetFileName()` specifies the input file. DICOM (Digital Imaging and Communications in Medicine) is the standard format for medical imaging data.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the image as a 2D texture. `GetProperty().SetColorWindow()` and `SetColorLevel()` map the scalar range to the displayable grayscale range.
- [vtkInteractorStyleImage](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleImage.html) provides 2D pan and zoom interaction suitable for image viewing.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().ParallelProjectionOn()` ensures the image is displayed without perspective distortion.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
