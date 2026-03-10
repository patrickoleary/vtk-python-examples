### Description

This example creates a colored elevation map from randomly perturbed grid points using vtkDelaunay2D for triangulation and vtkElevationFilter for height-based coloring. A 20×20 grid of points with random perturbation is triangulated into a surface and colored by z-value. It follows the VTK pipeline structure:

**Random Points → Delaunay2D → ElevationFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDelaunay2D](https://www.vtk.org/doc/nightly/html/classvtkDelaunay2D.html) triangulates the scattered 2D points into a connected surface mesh.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) maps height (z value) to a scalar field for color mapping, with low and high points set from the data bounds.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random perturbations for the grid points in x, y, and z.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the triangulated surface to graphics primitives, coloring by elevation scalars.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
