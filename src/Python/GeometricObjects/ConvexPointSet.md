### Description

This example demonstrates a convex point set cell — a 3D cell defined by a convex set of points, internally triangulated for rendering. Small spheres are glyphed at each vertex. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the convex hull with `EdgeVisibilityOn()` and the point glyphs in a contrasting color.
- [vtkConvexPointSet](https://www.vtk.org/doc/nightly/html/classvtkConvexPointSet.html) defines a 3D cell from a convex set of points. Uses ordered triangulation (vtkOrderedTriangulator) internally for compatible triangulations across shared faces.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives via `SetInputData()`.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places a sphere glyph at each point in the polydata via `SetSourceConnection()`.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 13 points: 8 cube corners plus 5 face-center points.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates small spheres used as glyphs at each vertex.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) stores the convex point set cell and its points.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a silver background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
