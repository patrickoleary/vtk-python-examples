### Description

This example visualizes a quadric function using isosurfaces, color-mapped planes, and contour lines.

**Quadric → SampleFunction → ContourFilter → Mapper → Actor | ExtractVOI → AppendFilter → Mapper → Actor | ExtractVOI → ContourFilter → AppendFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAppendFilter](https://www.vtk.org/doc/nightly/html/classvtkAppendFilter.html) combines multiple slices into one dataset.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) generates isosurfaces and contour lines.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps dataset data to graphics primitives.
- [vtkExtractVOI](https://www.vtk.org/doc/nightly/html/classvtkExtractVOI.html) extracts slices from the volume.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates bounding outlines.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkQuadric](https://www.vtk.org/doc/nightly/html/classvtkQuadric.html) defines the quadric implicit function.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) samples the quadric on a regular grid.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
