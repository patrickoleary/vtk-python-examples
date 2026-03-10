### Description

This example displays a photographic frog slice (upper-left), its tissue segmentation (upper-right), and a composite overlay (bottom) using texture-mapped planes.

**MetaImageReader → ImageConstantPad → Texture + PlaneSource → Mapper → Actor → Renderer × 3 → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkImageConstantPad](https://www.vtk.org/doc/nightly/html/classvtkImageConstantPad.html) extracts a single slice from each volume.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps tissue labels to colors for the segmentation.
- [vtkMatrix4x4](https://www.vtk.org/doc/nightly/html/classvtkMatrix4x4.html) head-first superior-to-inferior (hfsi) orientation.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) loads the photographic and segmented frog volumes.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) provides the textured quad geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes point and/or cell normals.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the slice image as a surface texture.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) orients the plane with a head-first superior-to-inferior transform.
- [vtkWindowLevelLookupTable](https://www.vtk.org/doc/nightly/html/classvtkWindowLevelLookupTable.html) maps greyscale values for the photograph.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
