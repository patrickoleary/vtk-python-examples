### Description

This example colors vertices of a directed graph using a lookup table. Three vertices are positioned explicitly along the x-axis and each is assigned an integer color index mapped to red, white, or green via a three-entry lookup table. A view theme applies the lookup table to point (vertex) colors.

**vtkMutableDirectedGraph + vtkPoints → vtkGraphLayoutView + vtkViewTheme (vertex colors via vtkLookupTable)**

- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the graph with colored vertices.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores the per-vertex color index.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps integer indices to colors.
- [vtkMutableDirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableDirectedGraph.html) builds the directed graph.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) positions vertices explicitly.
- [vtkViewTheme](https://www.vtk.org/doc/nightly/html/classvtkViewTheme.html) applies a point lookup table for vertex coloring.
