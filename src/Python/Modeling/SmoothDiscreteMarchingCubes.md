### Description

This example generates labeled blob volumes, extracts discrete isosurfaces with vtkDiscreteMarchingCubes, and smooths them using vtkWindowedSincPolyDataFilter. Each labeled region is rendered in a distinct random color. It follows the VTK pipeline structure:

**SampleFunction + ImageThreshold (×20) → DiscreteMarchingCubes → WindowedSincPolyDataFilter → Mapper + LookupTable → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the smoothed colored isosurfaces.
- [vtkDiscreteMarchingCubes](https://www.vtk.org/doc/nightly/html/classvtkDiscreteMarchingCubes.html) extracts isosurfaces for each discrete label value.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) represents a regular image or volume.
- [vtkImageMathematics](https://www.vtk.org/doc/nightly/html/classvtkImageMathematics.html) composites the labeled spheres into one volume using a max operation.
- [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html) labels each sphere with a unique integer ID.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) assigns a random color to each label.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) provides minimal standard random sequence functionality.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the smoothed isosurfaces with the color lookup table.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) samples an implicit function over a grid.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) and [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) create implicit sphere volumes sampled on a 100³ grid.
- [vtkWindowedSincPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkWindowedSincPolyDataFilter.html) smooths the discrete surfaces with 15 iterations and non-manifold smoothing enabled.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
