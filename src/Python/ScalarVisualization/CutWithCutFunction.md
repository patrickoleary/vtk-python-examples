### Description

This example cuts a surface model with a series of planes using vtkCutter.

**Reader → Cutter → Mapper → Actor | Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) cuts the model with evenly spaced planes.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the cutting plane.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) reads the polygonal surface model.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
