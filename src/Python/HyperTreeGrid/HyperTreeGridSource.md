### Description

This example creates a 3D hyper tree grid from a text descriptor string, converts it to an unstructured grid, shrinks the cells to reveal the adaptive refinement structure, and renders the result colored by the Depth scalar. It follows the VTK pipeline structure:

**Source → HTG-to-UG → Shrink → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid to graphics primitives. `SetScalarModeToUseCellFieldData()` and `SelectColorArray("Depth")` color each cell by its depth level.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field. `SetDimensions(4,4,3)` defines a 3×3×2 rectilinear grid of root cells. `SetBranchFactor(4)` means each refined cell splits into 4^d children (64 in 3D). `SetMaxDepth(6)` caps the tree depth. `SetDescriptor()` encodes the tree structure using `R` (refined) and `.` (leaf) characters separated by `|` between levels. `SetActiveScalars("Depth")` is called so downstream filters can find the scalar data.
- [vtkHyperTreeGridToUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridToUnstructuredGrid.html) converts the hyper tree grid into an unstructured grid so it can be rendered with standard VTK mappers.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) shrinks each cell toward its centroid. `SetShrinkFactor(0.8)` leaves small gaps that reveal the adaptive refinement structure.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view to show the 3D structure.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
