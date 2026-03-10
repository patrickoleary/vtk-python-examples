### Description

This example scales vertex glyphs by a data array. Two vertices are drawn as circles whose size reflects a "Scales" array, and whose color is driven by a lookup table with yellow and green entries.

**vtkMutableUndirectedGraph → vtkGraphLayoutView (scaled glyphs, vertex colors via vtkLookupTable)**

- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the graph with scaled vertex glyphs.
- [vtkGraphToGlyphs](https://www.vtk.org/doc/nightly/html/classvtkGraphToGlyphs.html) provides glyph type constants.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores integer data arrays.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps integer indices to colors.
- [vtkMutableUndirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableUndirectedGraph.html) builds the undirected graph.
- [vtkRenderedGraphRepresentation](https://www.vtk.org/doc/nightly/html/classvtkRenderedGraphRepresentation.html) sets the glyph type to circle.
- [vtkViewTheme](https://www.vtk.org/doc/nightly/html/classvtkViewTheme.html) applies a point lookup table for vertex coloring.
