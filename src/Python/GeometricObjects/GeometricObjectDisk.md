### Description

This example renders a 3D disk using [vtkDiskSource](https://www.vtk.org/doc/nightly/html/classvtkDiskSource.html). The source produces a polygonal disk (annulus) centered at the origin in the XY plane. It follows the standard VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties such as color.
- [vtkDiskSource](https://www.vtk.org/doc/nightly/html/classvtkDiskSource.html) generates disk poly data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
