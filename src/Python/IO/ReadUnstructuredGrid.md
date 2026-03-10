### Description

This example reads a VTK XML unstructured grid (.vtu) file and renders it with distinct front and back face colors using the standard VTK pipeline.

**Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the front face color. `SetBackfaceProperty()` assigns a separate [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) for back-facing faces with a contrasting color.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps any dataset type (including unstructured grids) to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkXMLUnstructuredGridReader](https://www.vtk.org/doc/nightly/html/classvtkXMLUnstructuredGridReader.html) reads a VTK XML unstructured grid (.vtu) file. `SetFileName()` specifies the input file.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
