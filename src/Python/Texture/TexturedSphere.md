### Description

This example maps an equirectangular earth texture onto a sphere using vtkTexturedSphereSource.

**TexturedSphereSource → TransformTextureCoords → Mapper + ImageReader → Texture → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry and texture.
- [vtkImageReader2Factory](https://www.vtk.org/doc/nightly/html/classvtkImageReader2Factory.html) automatically selects the correct image reader.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the earth image as a texture map.
- [vtkTexturedSphereSource](https://www.vtk.org/doc/nightly/html/classvtkTexturedSphereSource.html) generates a sphere with spherical texture coordinates.
- [vtkTransformTextureCoords](https://www.vtk.org/doc/nightly/html/classvtkTransformTextureCoords.html) shifts the texture coordinates to center the desired region.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
