### Description

This example bars chart of quarterly revenue data for two product lines using a chart overlay on the normal VTK rendering pipeline. Grouped bars allow direct comparison between categories.

**vtkTable → vtkChartXY (BAR plots) → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChart](https://www.vtk.org/doc/nightly/html/classvtkChart.html) provides chart functionality.
- [vtkChartXY](https://www.vtk.org/doc/nightly/html/classvtkChartXY.html) creates the 2D bar chart with axes and legend.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores revenue values.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores quarter indices.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the columnar data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
