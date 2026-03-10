### Description

This example scatters plot of trig functions using a chart overlay on the normal VTK rendering pipeline. Three series (cosine, sine, and sine-cosine) are plotted with different marker styles (cross, plus, circle) using vtkChartXY.

**vtkTable (trig data) → vtkChartXY → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChart](https://www.vtk.org/doc/nightly/html/classvtkChart.html) provides chart functionality.
- [vtkChartXY](https://www.vtk.org/doc/nightly/html/classvtkChartXY.html) creates the 2D scatter chart with axes and legend.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart's context scene on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotPoints](https://www.vtk.org/doc/nightly/html/classvtkPlotPoints.html) renders the scatter series with configurable marker styles.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the columnar data for the chart.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
