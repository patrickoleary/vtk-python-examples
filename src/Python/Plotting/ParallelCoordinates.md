### Description

This example parallels coordinates plot of multi-dimensional car attribute data. Each vertical axis represents a different attribute (horsepower, weight, MPG, cylinders, displacement) and each polyline connecting the axes represents one data sample. Interactive brushing on the axes allows filtering.

**vtkTable → vtkChartParallelCoordinates → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChartParallelCoordinates](https://www.vtk.org/doc/nightly/html/classvtkChartParallelCoordinates.html) creates the parallel coordinates chart with interactive axis brushing.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each attribute column.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random data.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the multi-dimensional data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
