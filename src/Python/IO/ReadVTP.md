### Description

This example reads a VTK XML PolyData (.vtp) file and renders the mesh with edge visibility enabled using the standard VTK pipeline.

**Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().EdgeVisibilityOn()` draws cell edges over the surface for a wireframe-on-solid effect.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) reads a VTK XML PolyData (.vtp) file. `SetFileName()` specifies the input file. VTP is VTK's native XML format for polygonal mesh data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
