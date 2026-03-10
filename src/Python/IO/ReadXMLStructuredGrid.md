### Description

This example reads a VTK XML structured grid (.vts) file using vtkXMLStructuredGridReader and display it with scalar coloring. A small sinusoidal surface is generated and written to disk if the file does not already exist.

**Reader → StructuredGridGeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkStructuredGrid.html) represents a structured grid with explicit point positions.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts surface geometry from a structured grid.
- [vtkXMLStructuredGridReader](https://www.vtk.org/doc/nightly/html/classvtkXMLStructuredGridReader.html) reads VTK XML structured grid files.
- [vtkXMLStructuredGridWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLStructuredGridWriter.html) writes VTK XML structured grid files (used to generate sample data).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
