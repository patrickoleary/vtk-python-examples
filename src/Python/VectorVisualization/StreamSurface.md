### Description

This example visualizes combustor flow with a stream surface generated from a rake of seed points.

**MultiBlockPLOT3DReader → StreamTracer (RK4, + LineSource) → RuledSurfaceFilter → Mapper → Actor | StructuredGridOutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkLineSource](https://www.vtk.org/doc/nightly/html/classvtkLineSource.html) generates a rake of seed points across the inlet.
- [vtkMultiBlockPLOT3DReader](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockPLOT3DReader.html) reads the combustor geometry and solution files.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRuledSurfaceFilter](https://www.vtk.org/doc/nightly/html/classvtkRuledSurfaceFilter.html) connects adjacent streamlines into a ruled surface.
- [vtkRungeKutta4](https://www.vtk.org/doc/nightly/html/classvtkRungeKutta4.html) provides fourth-order Runge-Kutta integration.
- [vtkStreamTracer](https://www.vtk.org/doc/nightly/html/classvtkStreamTracer.html) traces streamlines forward through the flow field.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates a bounding outline.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
