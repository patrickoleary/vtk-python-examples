### Description

This example interactivelies seed streamline ribbons in the combustor using two line widgets.

**MultiBlockPLOT3DReader → StreamTracer (+ LineWidget) → RibbonFilter → Mapper → Actor | StructuredGridOutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkLineWidget](https://www.vtk.org/doc/nightly/html/classvtkLineWidget.html) provides interactive seed lines (press **i** for widget 1, **L** for widget 2).
- [vtkMultiBlockPLOT3DReader](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockPLOT3DReader.html) reads the combustor geometry and solution files.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRibbonFilter](https://www.vtk.org/doc/nightly/html/classvtkRibbonFilter.html) converts streamlines into ribbons showing vorticity.
- [vtkRungeKutta4](https://www.vtk.org/doc/nightly/html/classvtkRungeKutta4.html) provides fourth-order Runge-Kutta integration.
- [vtkStreamTracer](https://www.vtk.org/doc/nightly/html/classvtkStreamTracer.html) traces streamlines through the flow field.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates a bounding outline.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
