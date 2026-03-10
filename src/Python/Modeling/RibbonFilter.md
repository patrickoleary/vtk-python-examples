### Description

This example creates ribbons from a helical polyline using vtkRibbonFilter. The original helix is shown as a tomato-red line alongside the cornflower-blue ribbon surface. It follows the VTK pipeline structure:

**Helix Points → PolyData → RibbonFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the ribbon surface (cornflower blue) and the helix line (tomato red).
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) and [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) define a 200-point helical polyline with four full turns.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the ribbon surface and original helix line to graphics primitives.
- [vtkRibbonFilter](https://www.vtk.org/doc/nightly/html/classvtkRibbonFilter.html) generates a ribbon surface from the polyline with a specified width and default normal.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
