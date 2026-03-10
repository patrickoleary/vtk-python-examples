### Description

This example converts an undirected graph with explicit vertex positions to vtkPolyData and render it using the standard 3D pipeline (mapper → actor → renderer). The graph has a star topology with four vertices.

**vtkMutableUndirectedGraph + vtkPoints → vtkGraphToPolyData → vtkPolyDataMapper → vtkActor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkGraphToPolyData](https://www.vtk.org/doc/nightly/html/classvtkGraphToPolyData.html) converts graph edges to polydata lines.
- [vtkMutableUndirectedGraph](https://www.vtk.org/doc/nightly/html/classvtkMutableUndirectedGraph.html) builds the undirected graph.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) positions vertices in 3D space.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
