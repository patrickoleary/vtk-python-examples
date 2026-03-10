### Description

This example visualizes a line-polygon intersection test. A unit square polygon lies in the x-y plane and a line segment crosses it along z. The intersection point is marked with a sphere glyph colored green (hit) or red (miss). It follows the VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties — semi-transparent light blue for the polygon, white for the line, and conditional color for the glyph.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) visualizes the test ray from p1 to p2.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each piece of geometry to graphics primitives.
- [vtkPolygon](https://www.vtk.org/doc/nightly/html/classvtkPolygon.html) defines a quadrilateral in the x-y plane. `IntersectWithLine()` tests whether a line segment pierces the polygon, returning the parametric coordinate and intersection point.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) creates a small glyph centered at the intersection point, colored green for a hit or red for a miss.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark green background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
