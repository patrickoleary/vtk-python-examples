### Description

This example demonstrates vtkCellQuality to compute the aspect ratio quality metric for each cell of a Delaunay triangulation and color the mesh by quality.

**PointSource → Delaunay2D → CellQuality → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellQuality](https://www.vtk.org/doc/nightly/html/classvtkCellQuality.html) computes a quality metric (aspect ratio, area, etc.) for each cell.
- [vtkDelaunay2D](https://www.vtk.org/doc/nightly/html/classvtkDelaunay2D.html) creates a 2D triangulation from the random points.
- [vtkPointSource](https://www.vtk.org/doc/nightly/html/classvtkPointSource.html) generates random points.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the quality-colored mesh to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
