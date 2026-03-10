### Description

This example demonstrates vtkSurfaceNets3D to extract a smooth isosurface from a procedural sinusoidal volume.

**ImageSinusoidSource → SurfaceNets3D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkImageSinusoidSource](https://www.vtk.org/doc/nightly/html/classvtkImageSinusoidSource.html) generates a procedural sinusoidal volume.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the isosurface to graphics primitives.
- [vtkSurfaceNets3D](https://www.vtk.org/doc/nightly/html/classvtkSurfaceNets3D.html) extracts smooth isosurfaces from labeled or scalar image data using a surface-nets algorithm.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
