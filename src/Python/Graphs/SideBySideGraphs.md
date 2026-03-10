### Description

This example displays two graphs side by side in split viewports within a single render window. The left viewport shows a triangle graph (three vertices, three edges) and the right shows a single-edge graph (two vertices, one edge), both using force-directed layouts with different background colors.

**Two vtkMutableUndirectedGraph → Two vtkGraphLayoutView (split viewports)**

- [vtkGraphLayoutView](https://www.vtk.org/doc/nightly/html/classvtkGraphLayoutView.html) displays graphs with layout strategies.
- [vtkMutableUndirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableUndirectedGraph.html) builds undirected graphs.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) positions vertices explicitly.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
