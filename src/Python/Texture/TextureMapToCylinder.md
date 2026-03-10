### Description

This example maps a procedural checkerboard texture onto a cylinder using vtkTextureMapToCylinder to generate cylindrical texture coordinates. The checkerboard pattern is created with vtkImageCanvasSource2D and wrapped around the cylinder surface. It follows the VTK pipeline structure:

**CylinderSource → TextureMapToCylinder → Mapper → Actor (with Texture) → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `SetTexture()` applies the checkerboard texture.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates a cylinder with 32 sides and end caps.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) creates a procedural 128×128 checkerboard pattern for the texture image.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) converts the image data into an OpenGL texture. `InterpolateOn()` enables bilinear filtering.
- [vtkTextureMapToCylinder](https://www.vtk.org/doc/nightly/html/classvtkTextureMapToCylinder.html) generates cylindrical (θ, z) texture coordinates for each point. `PreventSeamOn()` avoids a visible seam where the texture wraps.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
