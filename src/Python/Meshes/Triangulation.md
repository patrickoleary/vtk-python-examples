### Description

This example triangulates a set of 50 randomly scattered 2D points using vtkDelaunay2D and displays the resulting triangulation with visible edges. The Delaunay triangulation connects the points such that no point lies inside the circumcircle of any triangle, producing a well-conditioned mesh. It follows the VTK pipeline structure:

**Random Points → Delaunay2D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the triangulation with alice-blue faces and steel-blue edges.
- [vtkDelaunay2D](https://www.vtk.org/doc/nightly/html/classvtkDelaunay2D.html) computes the 2D Delaunay triangulation of the scattered point set, producing a triangle mesh.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates 50 reproducible random 2D points (z = 0) in the range [−5, 5].
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the triangulated surface to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
