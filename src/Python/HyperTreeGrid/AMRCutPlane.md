### Description

This example cuts an overlapping AMR dataset with an oblique plane using vtkAMRCutPlane. A two-level AMR dataset with a Gaussian pulse scalar field is cut with a plane normal to (1, 1, 0) through the center. The cut surface is rendered colored by the pulse value alongside block outlines. It follows the VTK pipeline structure:

**AMR Data → AMRCutPlane → CompositeDataGeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the cut surface and the block outlines.
- [vtkAMRCutPlane](https://www.vtk.org/doc/nightly/html/classvtkAMRCutPlane.html) cuts an overlapping AMR dataset with an arbitrary plane. `SetNormal()` and `SetCenter()` define the plane. `SetLevelOfResolution(1)` includes both AMR levels in the output.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) extracts the surface geometry from the composite output.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) renders the bounding boxes of each AMR block.
- [vtkOverlappingAMR](https://www.vtk.org/doc/nightly/html/classvtkOverlappingAMR.html) holds the two-level AMR dataset.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
