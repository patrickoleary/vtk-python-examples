### Description

This example linearly extrudes a star-shaped polygon along the Z axis using vtkLinearExtrusionFilter to create a 3D solid. The original star outline is displayed as a tomato-red wireframe alongside the cornflower-blue extruded solid. It follows the VTK pipeline structure:

**Points + Polygon → TriangleFilter → LinearExtrusionFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the extruded solid (cornflower blue) and the star outline (tomato red wireframe).
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkLinearExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkLinearExtrusionFilter.html) extrudes the polygon along the Z axis with capping enabled to form a closed solid.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) and [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) define an 8-point star-shaped polygon in the XY plane.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the extruded solid and original wireframe to graphics primitives.
- [vtkTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkTriangleFilter.html) triangulates the polygon so it renders correctly before extrusion.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
