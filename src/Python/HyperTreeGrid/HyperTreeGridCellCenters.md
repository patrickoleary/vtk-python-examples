### Description

This example extracts cell centers from a hyper tree grid using vtkHyperTreeGridCellCenters and renders them as sphere glyphs colored and sized by tree depth. Coarse (unrefined) cells appear as large red/yellow spheres while refined cells appear as small green/cyan spheres, making the adaptive resolution structure immediately visible. A translucent wireframe of the full HTG provides spatial context. It follows the VTK pipeline structure:

**Source → CellCenters → ArrayCalculator → Glyph3DMapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors are used — sphere glyphs colored by Depth at cell centers and a translucent context wireframe with `SetOpacity(0.15)` and `EdgeVisibilityOn()`.
- [vtkArrayCalculator](https://www.vtk.org/doc/nightly/html/classvtkArrayCalculator.html) computes `InverseDepth = 5 - Depth` so coarse cells receive large scale values and refined cells receive small ones.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places a sphere glyph at each cell center point. `SelectColorArray("Depth")` colors each glyph by depth level. `SetScaleArray("InverseDepth")` and `SetScaleModeToScaleByMagnitude()` size each glyph so coarse cells are large and refined cells are small.
- [vtkHyperTreeGridCellCenters](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridCellCenters.html) extracts the center point of every leaf cell in the hyper tree grid, producing a point set. The `Depth` cell data is converted to point data on the output. This is useful for placing glyphs, labels, or seeds for streamlines at cell locations.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface as a translucent wireframe for spatial context.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field. `SetActiveScalars("Depth")` is called so downstream filters can find the scalar data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the context wireframe to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a unit sphere used as the glyph shape.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
