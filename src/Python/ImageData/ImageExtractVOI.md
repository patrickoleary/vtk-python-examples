### Description

This example crops a sub-volume from a 3D medical dataset using [vtkExtractVOI](https://www.vtk.org/doc/nightly/html/classvtkExtractVOI.html) and render the result as an iso-surface with [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html). The FullHead volume is cropped to its central 128×128×60 region before contouring.

**Reader → ExtractVOI → FlyingEdges3D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkExtractVOI](https://www.vtk.org/doc/nightly/html/classvtkExtractVOI.html) extracts a Volume Of Interest (sub-region) from the image data.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts an iso-surface at scalar value 500.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the MetaImage (.mhd/.raw) CT volume.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the iso-surface polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
