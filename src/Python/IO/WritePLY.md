### Description

This example generates a sphere, writes it to a PLY file, reads it back, and renders the result using the standard VTK pipeline.

**Source → Writer → Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkPLYReader](https://www.vtk.org/doc/nightly/html/classvtkPLYReader.html) reads the written PLY file back, verifying the round-trip.
- [vtkPLYWriter](https://www.vtk.org/doc/nightly/html/classvtkPLYWriter.html) writes polydata to a PLY (Polygon File Format) file. `SetFileName()` specifies the output path. PLY is commonly used for 3D scanning and point cloud data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere polygon mesh used as sample data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
