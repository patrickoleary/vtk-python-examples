### Description

This example spiders (radar) plot of random food-texture data using vtkSpiderPlotActor. Five attributes (bitter, crispy, crunchy, salty, oily) are plotted for 12 data points, each with a randomly assigned color. The spider plot displays multivariate data on radial axes emanating from a center point.

**vtkDataObject (field data) → vtkSpiderPlotActor → Renderer → RenderWindow → Interactor**

- [vtkDataObject](https://www.vtk.org/doc/nightly/html/classvtkDataObject.html) holds the field data arrays for the plot.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores each attribute column.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random data and plot colors.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkSpiderPlotActor](https://www.vtk.org/doc/nightly/html/classvtkSpiderPlotActor.html) renders the radar chart with configurable axes, labels, and legend.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
