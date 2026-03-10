### Description

This example builds a two-level overlapping AMR dataset with scalar values computed from an implicit sphere function, then renders the block outlines and an iso-surface extracted at a threshold value.

**Implicit Sphere → Uniform Grids → Overlapping AMR → Outline + Contour → Renderer → Window → Interactor**

- [vtkAMRBox](https://www.vtk.org/doc/nightly/html/classvtkAMRBox.html) defines the spatial extent of each block in the AMR hierarchy.
- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors are used — gold wireframe outlines for the AMR blocks and a peach puff iso-surface. `GetProperty().SetColor()` sets each actor's color.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) aggregates composite contour output into one polydata.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an iso-surface at value 10.0 from the AMR dataset.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores the scalar values computed from the implicit function at each grid point.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates wireframe bounding boxes for each AMR block.
- [vtkOverlappingAMR](https://www.vtk.org/doc/nightly/html/classvtkOverlappingAMR.html) organizes the uniform grids into a two-level AMR hierarchy. `SetRefinementRatio()` specifies the ratio between levels.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the outline wireframe and iso-surface polydata to graphics primitives.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) provides an implicit sphere function. `EvaluateFunction()` computes the signed distance at each grid point.
- [vtkUniformGrid](https://www.vtk.org/doc/nightly/html/classvtkUniformGrid.html) represents regular grids at each AMR level. Three grids are created: one coarse (spacing 1.0) and two refined (spacing 0.5).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
