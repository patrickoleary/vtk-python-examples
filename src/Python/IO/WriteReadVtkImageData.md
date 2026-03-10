### Description

This example creates a vtkImageData, fills it with scalar values, writes it to a .vti file using vtkXMLImageDataWriter, reads it back with vtkXMLImageDataReader, and renders the result. The scalar values are set to `x + y + z` for each voxel, producing a gradient colored by the default lookup table. It follows the VTK pipeline structure:

**ImageData → Writer → Reader → ImageDataGeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `SetPointSize(5)` makes the data points more visible.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) creates a small 3×4×5 image data and fills each voxel with a scalar value.
- [vtkImageDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkImageDataGeometryFilter.html) converts the image data to polydata for rendering.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives. `SetScalarRange()` maps the scalar values to the full color range.
- [vtkXMLImageDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLImageDataReader.html) reads the `.vti` file back, demonstrating the write/read round-trip.
- [vtkXMLImageDataWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLImageDataWriter.html) writes the image data to a `.vti` XML file.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
