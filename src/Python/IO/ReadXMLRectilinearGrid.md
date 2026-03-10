### Description

This example reads a VTK XML rectilinear grid (.vtr) file using vtkXMLRectilinearGridReader and display it with scalar coloring. A small rectilinear grid with a distance field is generated and written to disk if the file does not already exist.

**Reader → RectilinearGridGeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRectilinearGrid](https://www.vtk.org/doc/nightly/html/classvtkRectilinearGrid.html) represents a rectilinear grid.
- [vtkRectilinearGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkRectilinearGridGeometryFilter.html) extracts surface geometry from a rectilinear grid.
- [vtkXMLRectilinearGridReader](https://www.vtk.org/doc/nightly/html/classvtkXMLRectilinearGridReader.html) reads VTK XML rectilinear grid files.
- [vtkXMLRectilinearGridWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLRectilinearGridWriter.html) writes VTK XML rectilinear grid files (used to generate sample data).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
