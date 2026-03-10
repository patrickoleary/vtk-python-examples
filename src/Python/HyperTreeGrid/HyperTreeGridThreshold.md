### Description

This example thresholds cells of a hyper tree grid by their depth level using vtkHyperTreeGridThreshold with a two-sided threshold, extracting only depth-2 cells (the middle refinement level). This isolates a single refinement level, showing exactly which cells in the grid live at that depth. A translucent wireframe of the full HTG provides context. It follows the VTK pipeline structure:

**Source → Threshold → Geometry → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors are used — the thresholded cells colored by Depth with `EdgeVisibilityOn()`, and the full HTG as a translucent wireframe with `SetOpacity(0.15)`.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of the thresholded and full HTG as polydata.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field. `SetActiveScalars("Depth")` is called so downstream filters can find the scalar data.
- [vtkHyperTreeGridThreshold](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridThreshold.html) keeps only cells whose scalar value falls within the specified range. `SetLowerThreshold(2.0)` and `SetUpperThreshold(2.0)` retain only cells at depth level 2, demonstrating a two-sided threshold that isolates a single refinement level. The filter operates directly on the HTG without conversion.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface polydata to graphics primitives. `SetScalarModeToUseCellFieldData()` and `SelectColorArray("Depth")` color the thresholded surface by the Depth scalar.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
