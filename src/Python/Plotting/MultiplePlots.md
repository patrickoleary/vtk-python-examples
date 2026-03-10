### Description

This example Side-by-side cosine and sine scatter plots using chart overlays on the normal VTK rendering pipeline. Each chart lives in its own viewport via a separate vtkRenderer, with a vtkContextActor providing the chart overlay.

**vtkTable (trig data) → vtkChartXY (×2) → vtkContextActor (×2) → Renderers (viewports) → RenderWindow → Interactor**

- [vtkAxis](https://www.vtk.org/doc/nightly/html/classvtkAxis.html) configures chart axis titles and grid pen colors.
- [vtkChart](https://www.vtk.org/doc/nightly/html/classvtkChart.html) provides chart functionality.
- [vtkChartXY](https://www.vtk.org/doc/nightly/html/classvtkChartXY.html) creates each 2D scatter chart with axes and title.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays each chart's context scene on its renderer.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotPoints](https://www.vtk.org/doc/nightly/html/classvtkPlotPoints.html) renders the scatter series with configurable marker styles.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the columnar data shared by both charts.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles each viewport.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
