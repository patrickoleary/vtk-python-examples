### Description

This example renders a sphere, captures the render window contents to a TIFF image file, and displays the scene.

**Source → Mapper → Actor → Renderer → Window → WindowToImageFilter → Writer → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with front and back face colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere polygon mesh. `SetCenter()` and `SetRadius()` configure the geometry.
- [vtkTIFFWriter](https://www.vtk.org/doc/nightly/html/classvtkTIFFWriter.html) writes the captured image to a TIFF file. TIFF supports lossless compression and is widely used in scientific imaging and publishing.
- [vtkWindowToImageFilter](https://www.vtk.org/doc/nightly/html/classvtkWindowToImageFilter.html) captures the render window contents as image data for writing.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
