### Description

This example Texture-map a JPEG image onto a sphere using spherical texture coordinates.

**SphereSource → TextureMapToSphere → Mapper → Actor + Texture(JPEGReader) → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry and texture.
- [vtkJPEGReader](https://www.vtk.org/doc/nightly/html/classvtkJPEGReader.html) loads the masonry texture image.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere polygon data.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the image as a surface texture.
- [vtkTextureMapToSphere](https://www.vtk.org/doc/nightly/html/classvtkTextureMapToSphere.html) generates spherical texture coordinates.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
