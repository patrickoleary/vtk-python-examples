### Description

This example slices a hyper tree grid with an oblique plane using vtkHyperTreeGridPlaneCutter. The cut surface is colored by the Depth scalar — red/yellow for coarse cells and green/cyan for refined cells — with black edges showing the adaptive cell boundaries. A translucent wireframe of the full HTG provides spatial context. It follows the VTK pipeline structure:

**Source → PlaneCutter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors are used — the cut surface colored by Depth with `EdgeVisibilityOn()` and `SetLineWidth(2)`, and the context wireframe with `SetOpacity(0.15)`.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface as a translucent wireframe for spatial context.
- [vtkHyperTreeGridPlaneCutter](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridPlaneCutter.html) slices the hyper tree grid with an implicit plane. `SetPlane(a, b, c, d)` defines the cutting plane by the equation ax+by+cz=d. The filter operates directly on the HTG without converting to an unstructured grid, producing a polydata slice that respects the adaptive refinement.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field. `SetActiveScalars("Depth")` is called so downstream filters can find the scalar data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cut surface and context polydata to graphics primitives. `SetScalarModeToUseCellFieldData()` and `SelectColorArray("Depth")` color the cut surface by the cell depth value.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
