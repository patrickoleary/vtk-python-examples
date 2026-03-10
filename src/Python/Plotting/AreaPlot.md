### Description

This example filleds area plot of a damped sine wave with its decay envelope using a chart overlay on the normal VTK rendering pipeline. The shaded area shows the oscillation while a dashed line traces the exponential decay envelope.

**vtkTable → vtkPlotArea + vtkPlotLine → vtkChartXY → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChart](https://www.vtk.org/doc/nightly/html/classvtkChart.html) provides chart functionality.
- [vtkChartXY](https://www.vtk.org/doc/nightly/html/classvtkChartXY.html) creates the 2D chart with axes and legend.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the columnar data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
