### Description

This example creates three coloured vertex cells at triangle corners, write to a .vtp file, and render.

**Points → Vertices → PolyData → Writer / Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores the vertex cell connectivity.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the three vertex positions.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the vertex geometry and colour data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the vertex data to graphics primitives.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) assigns distinct RGB colours to each vertex.
- [vtkXMLPolyDataWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataWriter.html) writes the coloured vertices to a `.vtp` file.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
