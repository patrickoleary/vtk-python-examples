### Description

This example demonstrates screen-facing 3D text using vtkBillboardTextActor3D, labeling three spheres at different positions in the scene. Unlike vtkFollower, billboard text actors are rendered as 2D text that stays fixed in screen space while anchored to a 3D world position.

**Sources → Mappers → Actors → Billboard Text → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the sphere color.
- [vtkBillboardTextActor3D](https://www.vtk.org/doc/nightly/html/classvtkBillboardTextActor3D.html) displays screen-facing 2D text anchored to a 3D world position. `SetInput()` sets the label text. `SetPosition()` places the anchor in world coordinates. `GetTextProperty()` controls font size, color, justification, and style. The text automatically reorients to face the camera during interaction.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere polygon meshes at three different positions.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
