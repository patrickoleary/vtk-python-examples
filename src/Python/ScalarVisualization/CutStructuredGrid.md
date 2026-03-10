### Description

This example cuts through a structured grid with a plane.

**Reader → Cutter → Mapper → Actor | GeometryFilter → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) cuts the structured grid with the plane.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the cut surface with scalar coloring.
- [vtkMultiBlockPLOT3DReader](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockPLOT3DReader.html) reads the PLOT3D combustor dataset.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the cutting plane.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts a computational plane for comparison.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates the bounding outline.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
