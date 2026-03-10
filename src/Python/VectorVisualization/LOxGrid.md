### Description

This example visualizes LOx post flow with streamtubes and all computational grid planes visible.

**MultiBlockPLOT3DReader → StreamTracer (+ StructuredGridGeometryFilter seeds) → TubeFilter → Mapper → Actor | StructuredGridGeometryFilter → Mapper → Actor | StructuredGridOutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to color.
- [vtkMultiBlockPLOT3DReader](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockPLOT3DReader.html) reads the PLOT3D LOx post geometry and solution files.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkStreamTracer](https://www.vtk.org/doc/nightly/html/classvtkStreamTracer.html) traces streamlines through the flow field.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts floor, sub-floor, post, fan, and seed geometry.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates a bounding outline.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) wraps streamlines in tubes for better visibility.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
