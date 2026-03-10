### Description

This example visualizes a directed graph with edge arrows. The graph is laid out with a Simple2D strategy via vtkGraphLayout, then arrow glyphs are placed near each edge endpoint using vtkGlyph3D on the edge glyph output of vtkGraphToPolyData. The view uses pass-through layout and edge strategies since positions are pre-computed.

**vtkMutableDirectedGraph → vtkGraphLayout → vtkGraphLayoutView + vtkGraphToPolyData → vtkGlyph3D (arrow glyphs)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) repeats the arrow glyph on all edges.
- [vtkGlyphSource2D](https://www.vtk.org/doc/nightly/html/classvtkGlyphSource2D.html) creates the arrow glyph shape.
- [vtkGraphLayout](https://www.vtk.org/doc/nightly/html/classvtkGraphLayout.html) computes vertex positions.
- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the laid-out graph.
- [vtkGraphToPolyData](https://www.vtk.org/doc/nightly/html/classvtkGraphToPolyData.html) converts graph edges to polydata with glyph output.
- [vtkMutableDirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableDirectedGraph.html) builds the directed graph.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps arrow polydata to graphics primitives.
- [vtkSimple2DLayoutStrategy](https://www.vtk.org/doc/nightly/html/classvtkSimple2DLayoutStrategy.html) provides the layout algorithm.
