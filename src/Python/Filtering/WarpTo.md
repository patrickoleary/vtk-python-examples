### Description

This example creates a tube around a vertical line using vtkTubeFilter, then warps the geometry toward a target point using vtkWarpTo to demonstrate geometric deformation.

**LineSource → TubeFilter → WarpTo → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the surface color.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the warped geometry to graphics primitives. `ScalarVisibilityOff()` disables color-mapping so the actor color is used.
- [vtkLineSource](https://www.vtk.org/doc/nightly/html/classvtkLineSource.html) generates a vertical line with 20 subdivisions.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) wraps a cylindrical tube around the line.
- [vtkWarpTo](https://www.vtk.org/doc/nightly/html/classvtkWarpTo.html) deforms the tube by moving each point toward a target position with a configurable scale factor.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
