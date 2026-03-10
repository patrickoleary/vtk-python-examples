### Description

This example graphs layout visualization of a random tree using the explicit VTK rendering pipeline. A vtkRandomGraphSource generates a tree with 100 vertices and weighted edges. The graph is laid out using a force-directed 2D strategy, converted to polydata, and rendered with sphere glyphs for vertices (colored by ID) and lines for edges (colored by weight).

**vtkRandomGraphSource → vtkGraphLayout → vtkGraphToPolyData → Edges (lines) + Vertices (glyphed spheres) → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places sphere glyphs at each vertex.
- [vtkGraphLayout](https://www.vtk.org/doc/nightly/html/classvtkGraphLayout.html) positions vertices using a layout strategy.
- [vtkGraphToPolyData](https://www.vtk.org/doc/nightly/html/classvtkGraphToPolyData.html) converts the graph to polydata for rendering.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors for edges and vertices.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polydata to graphics primitives.
- [vtkRandomGraphSource](https://www.vtk.org/doc/nightly/html/classvtkRandomGraphSource.html) generates a random tree graph.
- [vtkSimple2DLayoutStrategy](https://www.vtk.org/doc/nightly/html/classvtkSimple2DLayoutStrategy.html) applies force-directed layout in 2D.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
