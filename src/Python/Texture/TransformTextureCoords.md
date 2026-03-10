### Description

This example transforms texture coordinates on a textured sphere using vtkTransformTextureCoords to scale, translate, and flip the mapping. The left viewport shows the original spherical texture mapping and the right viewport shows the transformed result with doubled frequency, shifted position, and flipped R coordinate. It follows the VTK pipeline structure:

**SphereSource → TextureMapToSphere → TransformTextureCoords → Mapper → Actor (with Texture) → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the original and transformed texture mappings.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a procedural 128×128 checkerboard pattern for the texture image.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere with 40×40 resolution.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) converts the image data into an OpenGL texture. `RepeatOn()` enables tiling when texture coordinates exceed [0, 1].
- [vtkTextureMapToSphere](https://www.vtk.org/doc/nightly/html/classvtkTextureMapToSphere.html) generates spherical texture coordinates for the input geometry.
- [vtkTransformTextureCoords](https://www.vtk.org/doc/nightly/html/classvtkTransformTextureCoords.html) applies affine transformations to texture coordinates. `SetScale(2.0, 2.0, 1.0)` doubles the texture frequency, `SetPosition(0.25, 0.25, 0.0)` shifts the origin, and `SetFlipR(True)` mirrors along the R axis.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
