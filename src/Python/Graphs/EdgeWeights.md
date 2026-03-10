### Description

This example displays edge weights on a fully connected directed graph. The force-directed layout uses the weight values to influence vertex spacing, and edge labels show the numeric weights.

**vtkMutableDirectedGraph → vtkGraphLayoutView (force-directed layout, edge weight labels)**

- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores per-edge weight values.
- [vtkForceDirectedLayoutStrategy](https://www.vtk.org/doc/nightly/html/classvtkForceDirectedLayoutStrategy.html) provides force directed layout strategy functionality.
- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the graph with a force-directed layout.
- [vtkMutableDirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableDirectedGraph.html) builds the directed graph.
