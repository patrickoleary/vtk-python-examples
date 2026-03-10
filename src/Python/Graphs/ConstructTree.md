### Description

This example constructs a tree from a directed graph using AddChild, convert it to a vtkTree with CheckedShallowCopy, and display it with a hierarchical tree layout.

**vtkMutableDirectedGraph → vtkTree → vtkGraphLayoutView (tree layout)**

- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the tree with a hierarchical layout.
- [vtkMutableDirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableDirectedGraph.html) builds the directed graph using AddChild.
- [vtkTree](https://www.vtk.org/doc/nightly/html/classvtkTree.html) represents the validated tree structure.
