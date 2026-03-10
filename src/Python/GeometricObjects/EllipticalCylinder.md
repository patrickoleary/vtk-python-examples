### Description

This example creates an elliptical cylinder by extruding an elliptical cross-section along a vector. Front and back faces are shown with different colors. It follows the standard VTK pipeline structure:

**Data → Filter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the cylinder. `SetBackfaceProperty()` assigns a different color to back-facing polygons via [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html).
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) positions the view with `Azimuth()` and `Elevation()`.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) maps mouse motion to camera transformations.
- [vtkLinearExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkLinearExtrusionFilter.html) extrudes the elliptical cross-section along the z-axis via `SetVector()` to create the cylinder surface.
- [vtkMath](https://www.vtk.org/doc/nightly/html/classvtkMath.html) provides mathematical utility functions.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores points sampled along an ellipse with semi-axes r1 and r2.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the geometry to graphics primitives.
- [vtkPolyLine](https://www.vtk.org/doc/nightly/html/classvtkPolyLine.html) connects the ellipse points into a closed polyline stored in a [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html).
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a slate gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
