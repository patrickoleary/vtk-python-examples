### Description

This example displays an intermediate configuration of the Towers of Hanoi puzzle, captured mid-solve with a disk in flight between pegs.

**CylinderSource (pegs/pucks) + PlaneSource (table) → Mapper → Actor → animated transforms → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) switches to a close-up viewpoint at the captured moment.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates peg and puck geometry.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) assigns reproducible random colors to pucks.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates the table surface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
