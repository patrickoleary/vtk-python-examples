### Description

This example demonstrates text with a leader line pointing to a 3D position using vtkCaptionActor2D. Two captions label the tip and base of a cone, each with an arrow connecting the text to its attachment point in 3D space.

**Source → Mapper → Actor → Captions → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the cone color.
- [vtkCaptionActor2D](https://www.vtk.org/doc/nightly/html/classvtkCaptionActor2D.html) displays 2D text with a leader line connecting to a 3D attachment point. `SetAttachmentPoint()` specifies the 3D position the leader points to. `SetCaption()` sets the text label. `GetCaptionTextProperty()` controls font size, color, and style. `BorderOff()` removes the text border.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone polygon mesh.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
