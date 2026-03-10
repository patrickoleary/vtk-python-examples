### Description

This example computes and displays a histogram of scalar values from a 3D medical volume (FullHead.mhd). The left viewport shows the middle axial slice colored with a discrete cool-to-warm lookup table. The right viewport shows the histogram as a bar chart using vtkChartXY / vtkPlotBar rendered through vtkContextActor. It follows the VTK pipeline structure:

**Reader → ImageAccumulate → vtkTable → vtkChartXY (right viewport)**

- [vtkChartXY](https://www.vtk.org/doc/nightly/html/classvtkChartXY.html) creates a 2D bar chart. `AddPlot(0)` adds a bar plot and `SetInputData()` connects it to the table.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines a cool-to-warm diverging colormap used to build a discrete [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html).
- [vtkContextActor](https://www.vtk.org/doc/nightly/html/classvtkContextActor.html) hosts the chart scene inside a standard vtkRenderer, enabling the chart to coexist with 3D actors in the same window.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkImageAccumulate](https://www.vtk.org/doc/nightly/html/classvtkImageAccumulate.html) computes a histogram of the scalar values. `SetComponentExtent()` defines the number of bins.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the colormapped middle axial slice. `SetDisplayExtent()` selects a single Z value.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) applies the lookup table to the volume slice.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores integer data arrays.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume (256×256×94 voxels of signed short scalars).
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) holds the bin values and frequencies as columns for the chart.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
