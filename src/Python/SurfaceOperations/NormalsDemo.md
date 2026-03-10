### Description

This example surfaces normal generation comparison: faceted (left), shared normals (center), and split normals with a 30° feature angle (right).

**STLReader → PolyDataNormals → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between three viewports for synchronized viewing.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) generates surface normals with configurable feature angle and splitting.
- [vtkSTLReader](https://www.vtk.org/doc/nightly/html/classvtkSTLReader.html) loads the 42400-IDGH STL mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) three viewports comparing normal generation methods.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
