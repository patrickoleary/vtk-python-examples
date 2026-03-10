### Description

This example renders a stippled (dashed) line by creating a 1-D texture from a 16-bit pattern and applying it to a vtkLineSource via texture coords.

**Source → Texture → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores the texture coordinates used to map the stipple pattern along the line.
- [vtkImageCanvasSource2D](https://www.vtk.org/doc/nightly/html/classvtkImageCanvasSource2D.html) generates the 1-D stipple pattern image.
- [vtkLineSource](https://www.vtk.org/doc/nightly/html/classvtkLineSource.html) creates the input line segment.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the line polygon data to graphics primitives.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the stipple pattern image to the line.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
