### Description

This example maps a procedural checkerboard texture onto a warped plane using vtkTextureMapToPlane to generate planar texture coordinates. The plane is warped with a cosine ripple pattern via vtkWarpScalar, and the checkerboard pattern is projected onto it. It follows the VTK pipeline structure:

**PlaneSource → WarpScalar → TextureMapToPlane → Mapper → Actor (with Texture) → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `SetTexture()` applies the checkerboard texture.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a procedural 128×128 checkerboard pattern for the texture image.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates a high-resolution planar mesh with `SetResolution(50, 50)`.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) converts the image data into an OpenGL texture. `InterpolateOn()` enables bilinear filtering.
- [vtkTextureMapToPlane](https://www.vtk.org/doc/nightly/html/classvtkTextureMapToPlane.html) generates planar (s, t) texture coordinates by projecting points onto a best-fit plane. This works well even on warped surfaces since the texture coordinates are computed from the projection.
- [vtkWarpScalar](https://www.vtk.org/doc/nightly/html/classvtkWarpScalar.html) displaces points along the surface normal by a scalar value, creating a cosine ripple pattern.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
