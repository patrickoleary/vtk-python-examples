### Description

This example samples a Perlin noise implicit function on a volume grid using vtkSampleFunction and extracts an iso-surface at value 0 with vtkContourFilter, producing an organic-looking surface.

**PerlinNoise → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the surface color.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero-level iso-surface from the sampled volume.
- [vtkPerlinNoise](https://www.vtk.org/doc/nightly/html/classvtkPerlinNoise.html) defines a coherent noise implicit function with configurable frequency and phase.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the iso-surface to graphics primitives. `ScalarVisibilityOff()` disables color-mapping so the actor color is used.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit function on a 65x65x20 volume grid.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. `ResetCamera()` frames the iso-surface.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
