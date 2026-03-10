### Description

This example converts an overlapping AMR dataset to a multi-block dataset using vtkAMRToMultiBlockFilter. The converted blocks are rendered with edge visibility and colored by the Gaussian pulse scalar field. Block outlines from the original AMR structure are shown for context. It follows the VTK pipeline structure:

**AMR Data → AMRToMultiBlockFilter → CompositeDataGeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the converted block surfaces and the AMR outlines.
- [vtkAMRToMultiBlockFilter](https://www.vtk.org/doc/nightly/html/classvtkAMRToMultiBlockFilter.html) converts a vtkOverlappingAMR dataset into a vtkMultiBlockDataSet. Each AMR block becomes a block in the output, making the data compatible with general VTK filters that do not support AMR natively.
- [vtkCompositeDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataGeometryFilter.html) extracts the surface geometry from the multi-block output.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) renders the bounding boxes of each AMR block.
- [vtkOverlappingAMR](https://www.vtk.org/doc/nightly/html/classvtkOverlappingAMR.html) holds the two-level AMR dataset with a Gaussian pulse scalar field.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
