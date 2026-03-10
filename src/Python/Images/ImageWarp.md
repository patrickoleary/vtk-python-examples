### Description

This example reads a BMP image, converts it to grayscale luminance, extracts the image as a polygon mesh, warps the mesh perpendicular to the image plane using the luminance values, and textures the result with the original color image. It combines the imaging and graphics pipelines using vtkMergeFilter. It follows the VTK pipeline structure:

**BMPReader → ImageLuminance → ImageDataGeometryFilter → WarpScalar → MergeFilter → DataSetMapper → Actor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkBMPReader](https://www.vtk.org/doc/nightly/html/classvtkBMPReader.html) reads the `masonry.bmp` BMP image.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the merged data to graphics primitives.
- [vtkImageDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkImageDataGeometryFilter.html) extracts the image data as a flat polygon mesh.
- [vtkImageLuminance](https://www.vtk.org/doc/nightly/html/classvtkImageLuminance.html) converts the color image to grayscale for use as warp scalars.
- [vtkMergeFilter](https://www.vtk.org/doc/nightly/html/classvtkMergeFilter.html) combines the warped geometry with the original color scalars from the reader.
- [vtkWarpScalar](https://www.vtk.org/doc/nightly/html/classvtkWarpScalar.html) displaces mesh vertices perpendicular to the image plane by the luminance value.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
