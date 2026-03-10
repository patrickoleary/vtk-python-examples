### Description

This example creates a labelled tree with vertex and edge labels displayed using a mellow theme and a hierarchical tree layout. The tree is built from a directed graph using AddChild and converted to a vtkTree.

**vtkMutableDirectedGraph → vtkTree → vtkGraphLayoutView (tree layout, mellow theme)**

- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the tree with vertex and edge labels.
- [vtkMutableDirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableDirectedGraph.html) builds the directed graph using AddChild.
- [vtkStringArray](https://www.vtk.org/doc/nightly/html/classvtkStringArray.html) stores vertex and edge label strings.
- [vtkTree](https://www.vtk.org/doc/nightly/html/classvtkTree.html) represents the validated tree structure.
- [vtkViewTheme](https://www.vtk.org/doc/nightly/html/classvtkViewTheme.html) applies a mellow color scheme.
