### Description

This example generates smoothed surface models from a labeled segmentation volume using [vtkDiscreteFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkDiscreteFlyingEdges3D.html). Each label produces a separate isosurface that is smoothed with a windowed sinc filter and displayed in a single scene with a unique color per label. For an unsmoothed cube-based view, see [GenerateCubesFromLabels](../GenerateCubesFromLabels).

**Reader → DiscreteFlyingEdges3D → Smoother → Threshold → MaskFields → GeometryFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataObject](https://www.vtk.org/doc/nightly/html/classvtkDataObject.html) provides data object functionality.
- [vtkDataSetAttributes](https://www.vtk.org/doc/nightly/html/classvtkDataSetAttributes.html) provides data set attributes functionality.
- [vtkDiscreteFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkDiscreteFlyingEdges3D.html) generates isosurfaces for each discrete label value.
- [vtkGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkGeometryFilter.html) converts unstructured grid output to polydata.
- [vtkImageAccumulate](https://www.vtk.org/doc/nightly/html/classvtkImageAccumulate.html) computes a histogram to determine which labels are present.
- [vtkMaskFields](https://www.vtk.org/doc/nightly/html/classvtkMaskFields.html) strips scalar arrays for clean geometry.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the labeled MetaImage (.mhd/.zraw) segmentation volume.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkThreshold](https://www.vtk.org/doc/nightly/html/classvtkThreshold.html) isolates individual labels from the combined surface.
- [vtkWindowedSincPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkWindowedSincPolyDataFilter.html) smooths the label surfaces while preserving boundaries.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
