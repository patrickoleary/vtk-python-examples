### Description

This example bags plot of 2D correlated Gaussian data using a chart overlay on the normal VTK rendering pipeline. A bag plot is the bivariate generalization of a box plot — it shows the median point, the "bag" containing 50% of the data, and the "fence" boundary for outlier detection. Points are colored by density.

**vtkTable (X, Y, Density) → vtkPlotBag → vtkChartXY → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChart](https://www.vtk.org/doc/nightly/html/classvtkChart.html) provides chart functionality.
- [vtkChartXY](https://www.vtk.org/doc/nightly/html/classvtkChartXY.html) hosts the bag plot.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random samples.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotBag](https://www.vtk.org/doc/nightly/html/classvtkPlotBag.html) renders the statistical bag contour with median, bag, and fence regions.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the X, Y, and density columns.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
