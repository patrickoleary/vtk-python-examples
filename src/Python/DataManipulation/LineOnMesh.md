### Description

This example creates a random topography mesh from a 32×32 height field, smooths it with loop subdivision, then traces a spline line on the surface by casting vertical rays and finding intersections with vtkCellLocator.

**Random Height Field → Triangulated Mesh → Clean → Loop Subdivision → Cell Locator → Spline → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. The terrain actor uses `GetProperty().SetInterpolationToFlat()` for faceted shading. The spline actor uses `GetProperty().SetColor()` for red and `SetLineWidth(3)` for visibility.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkCellLocator](https://www.vtk.org/doc/nightly/html/classvtkCellLocator.html) finds intersections between vertical lines and the smoothed surface. `IntersectWithLine()` returns the 3D position of each intersection.
- [vtkCleanPolyData](https://www.vtk.org/doc/nightly/html/classvtkCleanPolyData.html) merges duplicate points so edges are shared.
- [vtkLoopSubdivisionFilter](https://www.vtk.org/doc/nightly/html/classvtkLoopSubdivisionFilter.html) smooths the mesh by adding triangles via loop subdivision.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates a parametric function.
- [vtkParametricSpline](https://www.vtk.org/doc/nightly/html/classvtkParametricSpline.html) fits a smooth curve through the intersection points. [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the spline into polydata.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives. Two mappers are used — one for the terrain mesh and one for the spline line.
- [vtkTriangle](https://www.vtk.org/doc/nightly/html/classvtkTriangle.html) and [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) build a triangulated surface from the height field with per-vertex RGB colors.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) stores unsigned char data arrays.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a preset camera position.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
