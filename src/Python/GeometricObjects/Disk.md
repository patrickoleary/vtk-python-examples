### Description

This example renders a disk (annulus) with a hole in the center using vtkDiskSource. It follows the standard VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties including color to the mapped geometry.
- [vtkDiskSource](https://www.vtk.org/doc/nightly/html/classvtkDiskSource.html) generates a flat polygonal disk with zero height. `SetInnerRadius()` and `SetOuterRadius()` control the hole size and outer extent. `SetRadialResolution()` and `SetCircumferentialResolution()` control the mesh density.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the disk geometry to graphics primitives via `SetInputConnection()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark green background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
