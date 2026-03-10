### Description

This example selects vertices and edges interactively on a random graph. Click on vertices or edges in the view; a selection callback prints the selected IDs and their field type to the console via the annotation link observer.

**vtkRandomGraphSource → vtkGraphLayoutView + vtkAnnotationLink (selection callback)**

- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays the graph and handles selection.
- [vtkRandomGraphSource](https://www.vtk.org/doc/nightly/html/classvtkRandomGraphSource.html) generates a random graph.
