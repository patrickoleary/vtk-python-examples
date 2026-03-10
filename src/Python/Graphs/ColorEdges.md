### Description

This example colors edges of a directed graph using a lookup table. Each edge is assigned an integer index that maps to a color in a two-entry lookup table (red and green). A view theme applies the lookup table to the edge (cell) colors.

**vtkMutableDirectedGraph → vtkGraphLayoutView + vtkViewTheme (edge colors via vtkLookupTable)**

- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the graph with a layout strategy.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores the per-edge color index.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps integer indices to colors.
- [vtkMutableDirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableDirectedGraph.html) builds the directed graph.
- [vtkSimple2DLayoutStrategy](https://www.vtk.org/doc/nightly/html/classvtkSimple2DLayoutStrategy.html) provides simple2dlayout strategy functionality.
- [vtkViewTheme](https://www.vtk.org/doc/nightly/html/classvtkViewTheme.html) applies a cell lookup table for edge coloring.
