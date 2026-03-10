### Description

This example reads an Exodus II file and renders the geometry colored by a nodal variable using the standard VTK pipeline.

**Reader → GeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) extracts the surface geometry from the multi-block output of the Exodus reader into a single `vtkPolyData`.
- [vtkExodusIIReader](https://www.vtk.org/doc/nightly/html/classvtkExodusIIReader.html) reads an Exodus II (.e) file. `SetFileName()` specifies the input file. `SetTimeStep()` selects the time step to display. `SetAllArrayStatus()` enables all nodal variable arrays for reading.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives with scalar coloring by the selected nodal variable.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
