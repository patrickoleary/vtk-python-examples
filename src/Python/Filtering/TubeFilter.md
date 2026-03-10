### Description

This example creates a helix from a set of points and wraps tubes around the line using vtkTubeFilter with radius varying by a scalar array, producing a visually dynamic 3D curve.

**Points → Helix Polyline + Scalars → TubeFilter (variable radius) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the tube geometry to graphics primitives.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) generates tubes around lines with radius controlled by the `TubeRadius` scalar array via `SetVaryRadiusToVaryRadiusByAbsoluteScalar()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
