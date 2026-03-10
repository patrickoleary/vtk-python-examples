### Description

This example generates a sphere, writes it to an STL file, reads it back, and renders the result using the standard VTK pipeline.

**Source → Writer → Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkSTLReader](https://www.vtk.org/doc/nightly/html/classvtkSTLReader.html) reads the written STL file back, verifying the round-trip.
- [vtkSTLWriter](https://www.vtk.org/doc/nightly/html/classvtkSTLWriter.html) writes polydata to an STL (stereolithography) file. `SetFileName()` specifies the output path. STL describes triangulated surfaces and is the standard format for 3D printing.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere polygon mesh used as sample data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
