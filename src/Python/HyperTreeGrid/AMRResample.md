### Description

This example resamples an overlapping AMR dataset onto a uniform grid using vtkAMRResampleFilter. The resampled surface is rendered with edge visibility and colored by the Gaussian pulse scalar field. Block outlines from the original AMR structure are shown for context. It follows the VTK pipeline structure:

**AMR Data → AMRResampleFilter → CompositeDataGeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the resampled surface and the AMR outlines.
- [vtkAMRResampleFilter](https://www.vtk.org/doc/nightly/html/classvtkAMRResampleFilter.html) resamples an overlapping AMR dataset onto a uniform rectilinear grid. `SetMin()` and `SetMax()` define the sampling region, `SetNumberOfSamples()` controls the resolution, and `SetDemandDrivenMode(0)` enables full resampling.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) extracts the surface geometry from the composite output.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) renders the bounding boxes of each AMR block.
- [vtkOverlappingAMR](https://www.vtk.org/doc/nightly/html/classvtkOverlappingAMR.html) holds the two-level AMR dataset with a Gaussian pulse scalar field.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives. `SetScalarModeToUseCellFieldData()` and `SelectColorArray("Gaussian-Pulse")` ensure the scalar array is picked up from the composite output.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
