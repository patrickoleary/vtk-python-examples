### Description

This example checks whether a polydata surface is closed by detecting boundary edges with vtkFeatureEdges. Reads cow.vtp and displays any open edges in red.

**Reader → FeatureEdges → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the cow surface and any boundary edges in contrasting colours.
- [vtkFeatureEdges](https://www.vtk.org/doc/nightly/html/classvtkFeatureEdges.html) extracts boundary edges to test if the mesh is closed (zero boundary edges means closed).
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cow surface and boundary edges to graphics primitives.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) loads `cow.vtp` from the data directory.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
