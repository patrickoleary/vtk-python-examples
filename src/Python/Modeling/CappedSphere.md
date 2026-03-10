### Description

This example creates a capped sphere by rotationally extruding a semicircular arc using vtkRotationalExtrusionFilter. The arc is built programmatically from trigonometric points and capped by dropping a perpendicular to the rotation axis. It follows the VTK pipeline structure:

**Arc Points → PolyData → RotationalExtrusionFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the capped sphere in khaki.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) provides line functionality.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) and [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) define a semicircular arc with a cap segment dropping to the axis.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the sphere surface to graphics primitives.
- [vtkRotationalExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkRotationalExtrusionFilter.html) sweeps the arc 360° to form a closed sphere surface.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera with an elevated view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
