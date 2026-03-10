### Description

This example clips a scanned image to create a letter B wireframe.

**Reader → GaussianSmooth → ImageDataGeometryFilter → ClipPolyData → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkClipPolyData](https://www.vtk.org/doc/nightly/html/classvtkClipPolyData.html) clips the geometry at a scalar threshold.
- [vtkImageDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkImageDataGeometryFilter.html) converts image data to polygonal geometry.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) smooths the image with a Gaussian kernel.
- [vtkPNMReader](https://www.vtk.org/doc/nightly/html/classvtkPNMReader.html) reads the scanned PGM image.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
