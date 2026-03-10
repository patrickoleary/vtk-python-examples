### Description

This example creates two overlapping spheres, tetrahedralizes them with vtkDelaunay3D, combines them with vtkAppendFilter, and uses vtkConnectivityFilter to show they form a single connected region. Because the spheres overlap, the filter identifies one region and assigns a uniform color. Compare with the Meshes ConnectivityExtractRegions example where separated spheres produce two distinct regions. It follows the VTK pipeline structure:

**Sphere 1 + Sphere 2 → Delaunay3D → AppendFilter → ConnectivityFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAppendFilter](https://www.vtk.org/doc/nightly/html/classvtkAppendFilter.html) merges the two tetrahedralized spheres into one dataset.
- [vtkConnectivityFilter](https://www.vtk.org/doc/nightly/html/classvtkConnectivityFilter.html) identifies connected regions and assigns a region ID scalar to each cell. Because the spheres overlap, only one region is found.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the connectivity-colored dataset to graphics primitives.
- [vtkDelaunay3D](https://www.vtk.org/doc/nightly/html/classvtkDelaunay3D.html) tetrahedralizes each sphere's surface points into a volumetric mesh.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates two spheres centered at (−0.5, 0, 0) and (0.5, 0, 0) so they overlap.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
