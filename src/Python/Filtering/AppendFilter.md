### Description

This example combines a vtkPolyData point cloud and a vtkUnstructuredGrid into a single dataset using vtkAppendFilter, then visualizes the merged result with sphere glyphs.

**Source 1 (PointSource) + Source 2 (Points) → AppendFilter → Mapper + Glyph3DMapper → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `SetPointSize()` makes raw points visible; glyph actor colors are set via `GetProperty().SetColor()`.
- [vtkAppendFilter](https://www.vtk.org/doc/nightly/html/classvtkAppendFilter.html) merges the polydata and unstructured grid into a single unstructured grid.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the combined dataset to graphics primitives. Connected to the append filter via `SetInputConnection()`.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places sphere glyphs at each merged point for visibility.
- [vtkPointSource](https://www.vtk.org/doc/nightly/html/classvtkPointSource.html) generates 5 random points as vtkPolyData.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) represents unstructured geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
