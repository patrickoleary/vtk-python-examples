### Description

This example maps a texture image onto a plane, demonstrating basic texture mapping in VTK. The vtkPlaneSource generates texture coordinates automatically, so the image maps directly onto the surface. The vtkImageReader2Factory selects the correct reader for the image format.

**ImageReader → Texture + PlaneSource → Mapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry and texture.
- [vtkImageReader2Factory](https://www.vtk.org/doc/nightly/html/classvtkImageReader2Factory.html) automatically selects the correct image reader for the given file.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates a plane with texture coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the loaded image as a texture map on the actor.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
