### Description

This example boxes plot comparing five random distributions with different spreads using a chart overlay on the normal VTK rendering pipeline. Raw samples are generated procedurally, then summarised into quartile statistics by vtkComputeQuartiles before being passed to vtkChartBox. The box plot displays minimum, first quartile, median, third quartile, and maximum for each distribution.

**vtkTable (raw) → vtkComputeQuartiles → vtkTable (quartiles) → vtkChartBox + vtkPlotBox → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChartBox](https://www.vtk.org/doc/nightly/html/classvtkChartBox.html) creates the box plot chart with labeled columns.
- [vtkComputeQuartiles](https://www.vtk.org/doc/nightly/html/classvtkComputeQuartiles.html) computes quartile summary statistics from raw samples.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random values for each distribution.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotBox](https://www.vtk.org/doc/nightly/html/classvtkPlotBox.html) renders individual box-and-whisker glyphs for each column.
- [vtkStatisticsAlgorithm](https://www.vtk.org/doc/nightly/html/classvtkStatisticsAlgorithm.html) provides statistics algorithm functionality.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the per-column data values.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
