### Description

This example parallels coordinates chart linked to a 3D view of the same data. The left viewport shows a vtkChartParallelCoordinates displaying four scalar attributes (RTData, elevation, gradient magnitude, Brownian magnitude) derived from a vtkRTAnalyticSource pipeline. The right viewport shows a 3D outline of the image data bounds with all points rendered and colored by elevation.

**vtkRTAnalyticSource → ImageGradient → BrownianPoints → ElevationFilter → vtkTable → vtkChartParallelCoordinates (left) + 3D points (right) → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkBrownianPoints](https://www.vtk.org/doc/nightly/html/classvtkBrownianPoints.html) adds random vector attributes.
- [vtkChartParallelCoordinates](https://www.vtk.org/doc/nightly/html/classvtkChartParallelCoordinates.html) creates the parallel coordinates chart.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the point data with scalar coloring.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) maps spatial position to a scalar value.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkImageGradient](https://www.vtk.org/doc/nightly/html/classvtkImageGradient.html) computes the gradient of the RTData field.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps elevation values to colors.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a wireframe outline of the data bounds.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRTAnalyticSource](https://www.vtk.org/doc/nightly/html/classvtkRTAnalyticSource.html) generates a 3D wavelet image data set.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the extracted scalar columns.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles each viewport.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
