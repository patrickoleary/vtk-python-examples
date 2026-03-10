### Description

This example builds a two-level overlapping AMR dataset with a Gaussian pulse scalar field and renders it with block outlines and an iso-surface colored by the pulse value. It follows the VTK pipeline structure:

**AMR Construction → Contour / Outline → Mapper → Actor → Renderer → Window → Interactor**

- [vtkAMRBox](https://www.vtk.org/doc/nightly/html/classvtkAMRBox.html) provides amrbox functionality.
- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry. Gold wireframe outlines show the block boundaries; the iso-surface is colored by scalar value.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) aggregates the composite contour output into one polydata for rendering.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an iso-surface at the half-maximum (0.5) of the Gaussian pulse.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores the Gaussian pulse values (`exp(-r²/2σ²)`) at every grid point.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) renders the AMR block bounding boxes as gold wireframes.
- [vtkOverlappingAMR](https://www.vtk.org/doc/nightly/html/classvtkOverlappingAMR.html) holds a two-level AMR hierarchy with `vtkUniformGrid` blocks and a Gaussian pulse scalar field. `Initialize([1, 2])` creates one coarse block (level 0) and two refined blocks (level 1). `SetRefinementRatio(0, 2)` specifies that level 1 cells are half the size of level 0 cells.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives. `SetScalarRange()` maps the Gaussian pulse scalar to the default color lookup table.
- [vtkUniformGrid](https://www.vtk.org/doc/nightly/html/classvtkUniformGrid.html) defines each AMR block as a regular grid with `SetOrigin()`, `SetSpacing()`, and `SetDimensions()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
