### Description

This example extracts the frog brain from a segmented tissue volume, shown as an unsmoothed iso-surface (left) and a Gaussian-smoothed iso-surface (right).

**MetaImageReader → ImageThreshold → [GaussianSmooth →] FlyingEdges3D → [WindowedSincSmooth → Normals →] Stripper → Mapper → Actor → Renderer × 2 → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts the iso-surface.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) blurs the thresholded volume before contouring.
- [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html) isolates the brain tissue label.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) loads the segmented frog tissue volume.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes point and/or cell normals.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) creates triangle strips and/or polylines.
- [vtkWindowedSincPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkWindowedSincPolyDataFilter.html) smooths the mesh geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
