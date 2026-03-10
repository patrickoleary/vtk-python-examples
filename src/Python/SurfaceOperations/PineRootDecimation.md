### Description

This example decimations and connectivities filtering to reduce a noisy pine root isosurface. The mesh is first decimated, then the largest connected region is extracted.

**MCubesReader → DecimatePro → ConnectivityFilter → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConnectivityFilter](https://www.vtk.org/doc/nightly/html/classvtkConnectivityFilter.html) extracts the largest connected region, removing noisy fragments.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the connectivity filter output to graphics primitives.
- [vtkDecimatePro](https://www.vtk.org/doc/nightly/html/classvtkDecimatePro.html) reduces the mesh triangle count.
- [vtkMCubesReader](https://www.vtk.org/doc/nightly/html/classvtkMCubesReader.html) loads the marching cubes triangulation of a pine root.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a bounding box outline for spatial context.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the outline to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
