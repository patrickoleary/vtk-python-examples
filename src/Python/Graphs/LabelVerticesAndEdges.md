### Description

This example labels both vertices and edges of an undirected graph. Vertices are labelled with integer IDs (yellow) and edges with floating-point weights (green), using a circular layout strategy.

**vtkMutableUndirectedGraph → vtkGraphLayoutView (circular layout, vertex + edge labels)**

- [vtkCircularLayoutStrategy](https://www.vtk.org/doc/nightly/html/classvtkCircularLayoutStrategy.html) arranges vertices in a circle.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores per-edge weight values.
- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the graph with labels.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores per-vertex ID values.
- [vtkMutableUndirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableUndirectedGraph.html) builds the undirected graph.
