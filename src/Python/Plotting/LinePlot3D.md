### Description

This example 3D line plot of a parametric helix using a chart overlay on the normal VTK rendering pipeline. The helix is defined as (cos(t), sin(t), t/2π) and rendered with vtkPlotLine3D inside a vtkChartXYZ. A synthetic mouse event rotates the chart to an oblique initial view.

**vtkTable (helix data) → vtkPlotLine3D → vtkChartXYZ → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChartXYZ](https://www.vtk.org/doc/nightly/html/classvtkChartXYZ.html) creates the 3D chart with axes.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkContextMouseEvent](https://www.vtk.org/doc/nightly/html/classvtkContextMouseEvent.html) simulates a mouse drag for initial rotation.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each coordinate column.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotLine3D](https://www.vtk.org/doc/nightly/html/classvtkPlotLine3D.html) renders a 3D polyline from tabular X, Y, Z data.
- [vtkRectf](https://www.vtk.org/doc/nightly/html/classvtkRectf.html) specifies the chart geometry.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the helix coordinates.
- [vtkVector2i](https://www.vtk.org/doc/nightly/html/classvtkVector2i.html) provides vector2i functionality.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
