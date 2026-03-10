### Description

This example displays three orthogonal image planes (sagittal, axial, coronal) together with skin and bone isosurfaces from a CT head dataset. Each plane uses a different [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) — grayscale, full-hue, and single-hue saturation ramp — to illustrate different color-mapping strategies.

**Reader → FlyingEdges3D → Stripper → Mapper → Actor + ImageMapToColors → ImageActor + OutlineFilter → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts skin and bone isosurfaces.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a 2D image slice on a quadrilateral plane.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) maps scalar values to RGBA through a lookup table.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) defines scalar-to-color mappings.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the MetaImage (.mhd/.raw) CT volume.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates a bounding box wireframe.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) converts triangles to triangle strips.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
