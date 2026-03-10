### Description

This example parallels coordinates view of multi-attribute image data using a chart overlay on the normal VTK rendering pipeline. A vtkRTAnalyticSource generates volumetric data which is processed through gradient, Brownian points, and elevation filters. Four scalar attributes (RTData, elevation, gradient magnitude, Brownian magnitude) are extracted into a vtkTable and displayed on parallel axes.

**vtkRTAnalyticSource → ImageGradient → BrownianPoints → ElevationFilter → vtkTable → vtkChartParallelCoordinates → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkBrownianPoints](https://www.vtk.org/doc/nightly/html/classvtkBrownianPoints.html) adds random vector attributes.
- [vtkChartParallelCoordinates](https://www.vtk.org/doc/nightly/html/classvtkChartParallelCoordinates.html) creates the parallel coordinates chart with interactive axis brushing.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) maps spatial position to a scalar value.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each data column.
- [vtkImageGradient](https://www.vtk.org/doc/nightly/html/classvtkImageGradient.html) computes the gradient of the RTData field.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkRTAnalyticSource](https://www.vtk.org/doc/nightly/html/classvtkRTAnalyticSource.html) generates a 3D wavelet image data set.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the extracted scalar columns.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
