### Description

This example slices an overlapping AMR dataset along an axis-aligned plane using vtkAMRSliceFilter. A two-level AMR dataset with a Gaussian pulse scalar field is sliced at Z = 5.0 and rendered colored by the pulse value. Block outlines show the AMR structure. It follows the VTK pipeline structure:

**AMR Data → AMRSliceFilter → CompositeDataGeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the slice surface and the block outlines.
- [vtkAMRSliceFilter](https://www.vtk.org/doc/nightly/html/classvtkAMRSliceFilter.html) extracts an axis-aligned slice from an overlapping AMR dataset. `SetNormal(2)` selects the Z axis, `SetOffsetFromOrigin(5.0)` sets the slice position, and `SetMaxResolution(1)` includes both AMR levels.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) extracts the surface geometry from the composite (multi-block) output of the slice filter.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) renders the bounding boxes of each AMR block for spatial context.
- [vtkOverlappingAMR](https://www.vtk.org/doc/nightly/html/classvtkOverlappingAMR.html) holds the two-level AMR dataset with a coarse grid and two refined blocks.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives. `SetScalarModeToUsePointFieldData()` and `SelectColorArray("Gaussian-Pulse")` ensure the scalar array is picked up from the composite output.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
