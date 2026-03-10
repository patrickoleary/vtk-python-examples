### Description

This example extracts connected regions from a mesh containing two separate spheres using vtkConnectivityFilter on polydata. Each connected region is assigned a unique ID and colored accordingly, making it easy to identify distinct components in a combined mesh. It follows the VTK pipeline structure:

**SphereSource × 2 → AppendPolyData → ConnectivityFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAppendPolyData](https://www.vtk.org/doc/nightly/html/classvtkAppendPolyData.html) combines both spheres into a single polydata with two disconnected components.
- [vtkConnectivityFilter](https://www.vtk.org/doc/nightly/html/classvtkConnectivityFilter.html) labels each connected region with a unique ID. `SetExtractionModeToAllRegions()` extracts all regions. `ColorRegionsOn()` assigns a "RegionId" scalar to each point.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the labeled mesh to graphics primitives, coloring by region ID.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) — two sphere sources generate non-overlapping spheres at different positions.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
