### Description

This example renders a regular pentagon with visible edges using vtkRegularPolygonSource and vtkShrinkPolyData. It follows the VTK pipeline structure:

**Source → Filter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties to the mapped geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the shrunk polygon to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines the backface color (tomato). The front face is banana with `EdgeVisibilityOn()` and thick edges.
- [vtkRegularPolygonSource](https://www.vtk.org/doc/nightly/html/classvtkRegularPolygonSource.html) generates a regular polygon with `SetNumberOfSides()` controlling the vertex count and `SetRadius()` setting the circumscribed circle radius.
- [vtkShrinkPolyData](https://www.vtk.org/doc/nightly/html/classvtkShrinkPolyData.html) shrinks each polygon toward its centroid, visually separating faces.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a silver background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
