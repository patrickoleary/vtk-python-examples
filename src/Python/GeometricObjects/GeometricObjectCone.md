### Description

This example renders a 3D cone using [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html). The source produces a polygonal cone centered at the origin. It follows the standard VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties such as color.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates cone poly data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
