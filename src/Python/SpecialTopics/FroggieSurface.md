### Description

This example constructs up to fifteen tissue surfaces from a segmented frog dataset. Tissue parameters are loaded from `Frog_mhd.json`. The skin is rendered translucent so that internal organs are visible.

**MetaImageReader → [IslandRemoval → ImageThreshold →] ImageShrink3D → [GaussianSmooth →] FlyingEdges3D → TransformPolyData → [WindowedSincSmooth →] Normals → Stripper → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCameraOrientationWidget](https://www.vtk.org/doc/nightly/html/classvtkCameraOrientationWidget.html) provides an interactive orientation gizmo.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts tissue iso-surfaces.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) blurs the volume before contouring.
- [vtkImageIslandRemoval2D](https://www.vtk.org/doc/nightly/html/classvtkImageIslandRemoval2D.html) removes small isolated regions from each tissue.
- [vtkImageShrink3D](https://www.vtk.org/doc/nightly/html/classvtkImageShrink3D.html) downsamples the volume.
- [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html) isolates each tissue label.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) maps mouse motion to camera transformations.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors.
- [vtkMatrix4x4](https://www.vtk.org/doc/nightly/html/classvtkMatrix4x4.html) orientation transforms keyed by acquisition order name.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) loads the photographic and segmented frog volumes.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes point and/or cell normals.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) creates triangle strips and/or polylines.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) orients tissue surfaces according to slice acquisition order.
- [vtkWindowedSincPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkWindowedSincPolyDataFilter.html) smooths mesh geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
