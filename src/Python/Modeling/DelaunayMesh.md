### Description

This example performs 2D Delaunay triangulation on 50 random points using vtkDelaunay2D. The mesh edges are displayed as tubes and vertices as sphere glyphs for a polished visualization. It follows the VTK pipeline structure:

**Random Points → Delaunay2D → ExtractEdges + TubeFilter + Glyph3D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: edge tubes and vertex spheres.
- [vtkDelaunay2D](https://www.vtk.org/doc/nightly/html/classvtkDelaunay2D.html) triangulates the point set into a 2D mesh.
- [vtkExtractEdges](https://www.vtk.org/doc/nightly/html/classvtkExtractEdges.html) extracts the triangle edges for tube display.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) and [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) place sphere glyphs at each vertex (hot pink).
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates 50 reproducible random 2D points.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the tubes and glyphs to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) wraps the edges in visible tubes (peacock blue).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
