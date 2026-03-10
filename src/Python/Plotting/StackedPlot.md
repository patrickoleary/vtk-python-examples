### Description

This example stackeds area plot of three data series using a chart overlay on the normal VTK rendering pipeline. The series represent hypothetical web traffic by device type (desktop, mobile, tablet) over 12 months. Each series is stacked on top of the previous, showing both individual contributions and the total.

**vtkTable → vtkChartXY (STACKED plots) → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChart](https://www.vtk.org/doc/nightly/html/classvtkChart.html) provides chart functionality.
- [vtkChartXY](https://www.vtk.org/doc/nightly/html/classvtkChartXY.html) creates the 2D chart with axes and legend.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotStacked](https://www.vtk.org/doc/nightly/html/classvtkPlotStacked.html) renders each stacked area series (added via `vtkChart.STACKED`).
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the columnar data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
