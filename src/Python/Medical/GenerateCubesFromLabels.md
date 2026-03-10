### Description

This example converts labeled voxels from a segmented frog-tissue volume into colored cubes. Each label in the range 1–29 is thresholded, shifted by half a voxel, converted to surface geometry, and displayed with scalar coloring. For smoothed surface models from the same data, see [GenerateModelsFromLabels](../GenerateModelsFromLabels).

**Reader → ImageWrapPad → Threshold → TransformFilter → GeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataObject](https://www.vtk.org/doc/nightly/html/classvtkDataObject.html) provides data object functionality.
- [vtkDataSetAttributes](https://www.vtk.org/doc/nightly/html/classvtkDataSetAttributes.html) provides data set attributes functionality.
- [vtkGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkGeometryFilter.html) converts unstructured grid output to polydata for rendering.
- [vtkImageWrapPad](https://www.vtk.org/doc/nightly/html/classvtkImageWrapPad.html) extends the volume by one voxel so point data can become cell data.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the labeled MetaImage (.mhd/.zraw) segmentation volume.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives with scalar coloring.
- [vtkThreshold](https://www.vtk.org/doc/nightly/html/classvtkThreshold.html) selects cells within the specified label range.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformFilter.html) shifts geometry by half a voxel to align cubes with labels.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
