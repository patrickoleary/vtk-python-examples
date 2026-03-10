### Description

This example visualizes air convection in a kitchen using streamlines seeded from a rake under the window.

**StructuredGridReader → StreamTracer (+ LineSource) → Mapper → Actor | StructuredGridGeometryFilter → Mapper → Actor | StructuredGridOutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkLineSource](https://www.vtk.org/doc/nightly/html/classvtkLineSource.html) defines the seed rake for streamlines.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkStreamTracer](https://www.vtk.org/doc/nightly/html/classvtkStreamTracer.html) traces streamlines through the flow field.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts furniture surfaces for context.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates a bounding outline.
- [vtkStructuredGridReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridReader.html) reads the kitchen flow simulation.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
