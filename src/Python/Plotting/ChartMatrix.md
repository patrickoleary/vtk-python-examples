### Description

This example grids of four sub-charts arranged in a 2×2 layout using vtkChartMatrix. Each sub-chart shows a different trig function: sin(x), cos(x), sin(2x), and cos(2x). The top row uses line plots while the bottom row uses scatter plots, demonstrating how vtkChartMatrix arranges multiple independent charts in a single context scene.

**vtkTable → vtkChartMatrix (2×2 grid of vtkChartXY) → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChart](https://www.vtk.org/doc/nightly/html/classvtkChart.html) provides chart functionality.
- [vtkChartMatrix](https://www.vtk.org/doc/nightly/html/classvtkChartMatrix.html) arranges multiple charts in a grid layout.
- [vtkChartXY](https://www.vtk.org/doc/nightly/html/classvtkChartXY.html) creates each sub-chart with axes.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart matrix on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotPoints](https://www.vtk.org/doc/nightly/html/classvtkPlotPoints.html) renders scatter series in the bottom row.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the shared data.
- [vtkVector2f](https://www.vtk.org/doc/nightly/html/classvtkVector2f.html) provides vector2f functionality.
- [vtkVector2i](https://www.vtk.org/doc/nightly/html/classvtkVector2i.html) provides vector2i functionality.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
