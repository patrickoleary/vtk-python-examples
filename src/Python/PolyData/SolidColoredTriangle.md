### Description

This example builds a triangle with a single solid cell colour, write it to a .vtp file, and render it.

**Points → Triangle → PolyData → Writer / Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores the triangle cell connectivity.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the three triangle vertices.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the triangle geometry and colour data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the triangle polygon data to graphics primitives.
- [vtkTriangle](https://www.vtk.org/doc/nightly/html/classvtkTriangle.html) defines the triangle cell type with three point IDs.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) assigns a single solid colour to the cell.
- [vtkXMLPolyDataWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataWriter.html) writes the coloured triangle to a `.vtp` file.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
