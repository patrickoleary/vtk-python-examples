### Description

This example colors vertex labels of a directed graph. Each vertex is labelled with its integer ID and the label text is rendered in red by accessing the vertex label text property on the rendered graph representation.

**vtkMutableDirectedGraph → vtkGraphLayoutView + vtkRenderedGraphRepresentation (red vertex labels)**

- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the graph with vertex labels.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores the per-vertex label values.
- [vtkMutableDirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableDirectedGraph.html) builds the directed graph.
- [vtkRenderedGraphRepresentation](https://www.vtk.org/doc/nightly/html/classvtkRenderedGraphRepresentation.html) provides access to label text properties.
