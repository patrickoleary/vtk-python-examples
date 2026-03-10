### Description

This example stores three triangle corner points in a polydata, write to a .vtp file, and render.

**Points → PolyData → VertexGlyphFilter → Writer / Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the three corner positions.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the point geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the vertex data to graphics primitives.
- [vtkVertexGlyphFilter](https://www.vtk.org/doc/nightly/html/classvtkVertexGlyphFilter.html) converts the points into renderable vertex cells.
- [vtkXMLPolyDataWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataWriter.html) writes the vertices to a `.vtp` file.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
