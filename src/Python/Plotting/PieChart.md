### Description

This example pies chart of browser market share data using a chart overlay on the normal VTK rendering pipeline. Each slice is labeled and colored to represent a different browser's market share percentage.

**vtkTable → vtkPlotPie → vtkChartPie → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChartPie](https://www.vtk.org/doc/nightly/html/classvtkChartPie.html) creates the pie chart with title and legend.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) provides predefined color palettes.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores the slice values.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkStringArray](https://www.vtk.org/doc/nightly/html/classvtkStringArray.html) stores the slice labels.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the label, value, and color data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
