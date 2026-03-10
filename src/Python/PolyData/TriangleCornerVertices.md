### Description

This example creates vertex cells at triangle corner positions, write to a .vtp file, and render.

**Points → Vertices → PolyData → Writer / Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) creates individual vertex cells at each corner.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the three corner positions.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) stores the vertex geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the vertex data to graphics primitives.
- [vtkXMLPolyDataWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataWriter.html) writes the vertices to a `.vtp` file.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
