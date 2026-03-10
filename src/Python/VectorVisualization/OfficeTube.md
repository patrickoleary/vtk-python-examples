### Description

This example visualizes office airflow with a single streamtube whose radius varies by velocity magnitude.

**DataSetReader → StreamTracer (RK4) → TubeFilter → Mapper → Actor | StructuredGridGeometryFilter → Mapper → Actor | StructuredGridOutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkDataObject](https://www.vtk.org/doc/nightly/html/classvtkDataObject.html) provides data object functionality.
- [vtkDataSetReader](https://www.vtk.org/doc/nightly/html/classvtkDataSetReader.html) reads the office CFD structured grid.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRungeKutta4](https://www.vtk.org/doc/nightly/html/classvtkRungeKutta4.html) provides fourth-order Runge-Kutta integration.
- [vtkStreamTracer](https://www.vtk.org/doc/nightly/html/classvtkStreamTracer.html) traces a single streamline in both directions.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts furniture surfaces for context.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates a bounding outline.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) wraps the streamline in a tube with radius proportional to velocity.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
