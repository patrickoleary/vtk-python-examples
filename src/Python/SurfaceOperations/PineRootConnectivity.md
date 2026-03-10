### Description

This example connectivities filter to extract the largest region from a noisy pine root isosurface. Compare with [PineRootConnectivityA](../PineRootConnectivityA) which shows the raw unfiltered data.

**MCubesReader → PolyDataConnectivityFilter → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkMCubesReader](https://www.vtk.org/doc/nightly/html/classvtkMCubesReader.html) loads the marching cubes triangulation of a pine root.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a bounding box outline for spatial context.
- [vtkPolyDataConnectivityFilter](https://www.vtk.org/doc/nightly/html/classvtkPolyDataConnectivityFilter.html) extracts the largest connected region, removing noisy fragments.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
