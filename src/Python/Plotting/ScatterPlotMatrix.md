### Description

This example nxns scatter plot matrix of four correlated random variables (height, weight, age, income). The diagonal shows histograms, and each off-diagonal cell shows a scatter plot of one variable versus another. This is a standard exploratory data analysis tool for finding pairwise correlations in multivariate data.

**vtkTable → vtkScatterPlotMatrix → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each variable column.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random data.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkScatterPlotMatrix](https://www.vtk.org/doc/nightly/html/classvtkScatterPlotMatrix.html) creates the NxN grid of scatter plots with diagonal histograms.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) stores the multivariate data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
