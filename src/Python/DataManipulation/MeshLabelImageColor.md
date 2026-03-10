### Description

This example reads a label image in Meta format, extracts a surface mesh for a single label using discrete flying edges, smooths the mesh with a windowed sinc filter, and colors vertices by the smoothing displacement error using a diverging green-to-red color map.

**Reader → Extract VOI → Discrete Flying Edges → Windowed Sinc Smoother → Normals → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Scalar coloring from the smoothing error drives the surface appearance.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines a diverging green-to-red color map. The transfer function is sampled into a [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) for scalar coloring.
- [vtkDiscreteFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkDiscreteFlyingEdges3D.html) extracts a surface mesh for a selected label value from the segmented volume.
- [vtkExtractVOI](https://www.vtk.org/doc/nightly/html/classvtkExtractVOI.html) selects a volume of interest from the image data.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads a label image in `.mhd` format with an associated `.raw` binary data file.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the smoothed mesh to graphics primitives, colored by the smoothing error.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes cell normals for better lighting and visibility.
- [vtkWindowedSincPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkWindowedSincPolyDataFilter.html) smooths the mesh. `GenerateErrorScalarsOn()` produces per-vertex displacement error scalars showing how far each vertex moved during smoothing.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
