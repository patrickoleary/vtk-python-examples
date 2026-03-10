### Description

This example reads an STL mesh, writes it to a Wavefront OBJ file, reads it back, and renders the result using the standard VTK pipeline.

**STL Reader → OBJ Writer → OBJ Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with front and back face colors.
- [vtkOBJReader](https://www.vtk.org/doc/nightly/html/classvtkOBJReader.html) reads the written OBJ file back, verifying the round-trip.
- [vtkOBJWriter](https://www.vtk.org/doc/nightly/html/classvtkOBJWriter.html) writes polydata to a Wavefront OBJ (.obj) file. OBJ is a widely used text-based format for 3D geometry in modeling and game engines.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkSTLReader](https://www.vtk.org/doc/nightly/html/classvtkSTLReader.html) reads a stereolithography (.stl) file. `SetFileName()` specifies the input mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
