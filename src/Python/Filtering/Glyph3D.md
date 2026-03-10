### Description

This example places 3D cube glyphs at three points along the diagonal using vtkGlyph3D with a vtkCubeSource as the glyph shape.

**Points → CubeSource → Glyph3D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the glyph color.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates the cube used as the glyph shape.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) copies a source geometry to each input point in 3D space.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the glyphed output to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
