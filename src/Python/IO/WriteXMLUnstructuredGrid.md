### Description

This example builds a hexahedron cell, writes it to a VTK XML unstructured grid (.vtu) file, reads it back, and renders the result using the standard VTK pipeline.

**Cell Construction → Writer → Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with front and back face colors.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives.
- [vtkHexahedron](https://www.vtk.org/doc/nightly/html/classvtkHexahedron.html) defines a linear hexahedral cell by referencing the point IDs.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) assembles the points and cell into an unstructured grid dataset.
- [vtkXMLDataSetWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLDataSetWriter.html) save to XML unstructured grid file.
- [vtkXMLUnstructuredGridReader](https://www.vtk.org/doc/nightly/html/classvtkXMLUnstructuredGridReader.html) reads the written file back, verifying the round-trip.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
