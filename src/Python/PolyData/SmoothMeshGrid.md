### Description

This example compares Loop and Butterfly subdivision filters on a random-height mesh grid. Left: initial terrain, middle: vtkLoopSubdivisionFilter, right: vtkButterflySubdivisionFilter.

**Points → Triangles → Subdivision → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkButterflySubdivisionFilter](https://www.vtk.org/doc/nightly/html/classvtkButterflySubdivisionFilter.html) performs Butterfly interpolating subdivision.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores the triangle cell connectivity.
- [vtkCleanPolyData](https://www.vtk.org/doc/nightly/html/classvtkCleanPolyData.html) merges duplicate points before subdivision.
- [vtkLoopSubdivisionFilter](https://www.vtk.org/doc/nightly/html/classvtkLoopSubdivisionFilter.html) performs Loop approximating subdivision.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random heights for the grid vertices.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the grid vertex positions.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the mesh geometry and colour data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the mesh to graphics primitives.
- [vtkTriangle](https://www.vtk.org/doc/nightly/html/classvtkTriangle.html) defines each triangle cell in the grid.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) assigns per-cell colours to the mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
