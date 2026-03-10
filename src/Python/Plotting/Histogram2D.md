### Description

This example 2D histogram (heatmap) of correlated Gaussian random data using a chart overlay on the normal VTK rendering pipeline. 50,000 random samples are generated with Box-Muller and binned into a 60×60 grid stored as vtkImageData. A color transfer function maps bin counts from white (empty) through blue to red (dense).

**vtkImageData (bin counts) → vtkChartHistogram2D → vtkContextActor → Renderer → RenderWindow → Interactor**

- [vtkChartHistogram2D](https://www.vtk.org/doc/nightly/html/classvtkChartHistogram2D.html) displays a 2D histogram from image data.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) maps bin counts to RGB colors.
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) overlays the chart on the VTK rendering pipeline.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) stores the 2D bin grid.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random samples.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlotHistogram2D](https://www.vtk.org/doc/nightly/html/classvtkPlotHistogram2D.html) renders the heatmap with a color transfer function.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
