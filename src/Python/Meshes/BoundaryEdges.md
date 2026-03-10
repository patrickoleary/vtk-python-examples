### Description

This example extracts and highlights boundary edges of a disk mesh using vtkFeatureEdges. A disk with inner and outer boundary rings is generated, and only boundary edges are extracted and rendered in color on top of the light-grey disk surface. It follows the VTK pipeline structure:

**DiskSource → FeatureEdges → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors display the colored boundary edges and the light-grey disk surface.
- [vtkDiskSource](https://www.vtk.org/doc/nightly/html/classvtkDiskSource.html) generates an annular disk polygon with inner and outer boundary rings.
- [vtkFeatureEdges](https://www.vtk.org/doc/nightly/html/classvtkFeatureEdges.html) extracts only boundary edges. `BoundaryEdgesOn()` enables boundary extraction while `FeatureEdgesOff()`, `ManifoldEdgesOff()`, and `NonManifoldEdgesOff()` disable other edge types.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the boundary edges and the full disk surface to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
