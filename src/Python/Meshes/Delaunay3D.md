### Description

This example computes a 3D Delaunay tetrahedralization from 100 random points using vtkDelaunay3D and extracts the outer boundary surface with vtkGeometryFilter. The result is a translucent convex hull with visible edges. It follows the VTK pipeline structure:

**Random Points → Delaunay3D → GeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the convex hull with alice-blue faces, steel-blue edges, and 70% opacity.
- [vtkDelaunay3D](https://www.vtk.org/doc/nightly/html/classvtkDelaunay3D.html) computes the 3D Delaunay tetrahedralization of the point cloud, producing an unstructured grid of tetrahedra.
- [vtkGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkGeometryFilter.html) extracts the outer boundary surface (convex hull faces) from the tetrahedral mesh.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates 100 reproducible random 3D points in [−1, 1]³.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the boundary surface to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
