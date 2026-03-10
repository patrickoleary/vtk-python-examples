### Description

This example builds a two-level overlapping AMR dataset with a Gaussian pulse scalar field, writes it to the VTKHDF file format using vtkHDFWriter, reads it back with vtkHDFReader, and renders block outlines and an iso-surface of the round-tripped data. It follows the VTK pipeline structure:

**AMR Construction → Writer → Reader → Contour / Outline → Mapper → Actor → Renderer → Window → Interactor**

- [vtkAMRBox](https://www.vtk.org/doc/nightly/html/classvtkAMRBox.html) describes the index-space extent of each block in the AMR hierarchy.
- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors are used — gold wireframe block outlines with `SetLineWidth(2)` and a peach puff iso-surface.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) aggregates the composite contour output into one polydata for rendering.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an iso-surface at the half-maximum value (0.5) of the Gaussian pulse.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkHDFReader](https://www.vtk.org/doc/nightly/html/classvtkHDFReader.html) reads the VTKHDF file back, producing the same AMR dataset.
- [vtkHDFWriter](https://www.vtk.org/doc/nightly/html/classvtkHDFWriter.html) writes the overlapping AMR dataset to a `.vtkhdf` file. `SetOverwrite(True)` replaces an existing file. The VTKHDF format stores the AMR hierarchy, refinement ratios, and all block data in a single HDF5 file.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) shows the bounding boxes of the AMR blocks.
- [vtkOverlappingAMR](https://www.vtk.org/doc/nightly/html/classvtkOverlappingAMR.html) holds a two-level adaptive mesh refinement hierarchy. `Initialize([1, 2])` creates one coarse block (level 0) and two refined blocks (level 1). `SetRefinementRatio(0, 2)` specifies that level 1 cells are half the size of level 0 cells.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the outline and contour polydata to graphics primitives.
- [vtkUniformGrid](https://www.vtk.org/doc/nightly/html/classvtkUniformGrid.html) defines each AMR block as a regular grid with `SetOrigin()`, `SetSpacing()`, and `SetDimensions()`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
