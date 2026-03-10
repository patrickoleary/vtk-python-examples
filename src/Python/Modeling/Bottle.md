### Description

This example creates a bottle by rotationally extruding a hand-built profile polyline using vtkRotationalExtrusionFilter. The profile is also displayed as a tomato-red tube alongside the mint-green bottle surface. It follows the VTK pipeline structure:

**Points + Lines → PolyData → RotationalExtrusionFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the bottle surface (mint) and the profile tube (tomato red).
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) and [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) define the bottle profile as a 10-point polyline.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the bottle surface and profile tube to graphics primitives.
- [vtkRotationalExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkRotationalExtrusionFilter.html) sweeps the profile 360° around the Y axis with 60-step resolution to form the bottle surface.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) and [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) wrap the original profile polyline in a visible tube.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) generates tubes around lines.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
