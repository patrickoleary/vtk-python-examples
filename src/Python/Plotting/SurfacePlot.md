### Description

This example 3D surface plot of sin(sqrt(x² + y²)) using a chart overlay on the normal VTK rendering pipeline. The surface is rendered with vtkChartXYZ and vtkPlotSurface in a 3D chart that supports interactive rotation.

**vtkTable (surface data) → vtkPlotSurface → vtkChartXYZ → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChartXYZ](https://www.vtk.org/doc/nightly/html/classvtkChartXYZ.html) creates the 3D chart with axes.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart's context scene on the VTK rendering pipeline.
- [vtkContextMouseEvent](https://www.vtk.org/doc/nightly/html/classvtkContextMouseEvent.html) simulates a mouse drag to set the initial chart rotation.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each table column.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotSurface](https://www.vtk.org/doc/nightly/html/classvtkPlotSurface.html) renders the surface from tabular data.
- [vtkRectf](https://www.vtk.org/doc/nightly/html/classvtkRectf.html) specifies the chart geometry within the window.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the 2D grid of surface values.
- [vtkVector2i](https://www.vtk.org/doc/nightly/html/classvtkVector2i.html) provides vector2i functionality.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
