### Description

This example demonstrates 3D text annotation using vtkVectorText and vtkFollower to label the origin of a coordinate axes display. The text always faces the active camera so it remains readable from any viewing angle.

**Axes → Text Source → Follower → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the axes geometry to the scene.
- [vtkAxes](https://www.vtk.org/doc/nightly/html/classvtkAxes.html) generates XYZ coordinate axes at the origin as colored line segments.
- [vtkFollower](https://www.vtk.org/doc/nightly/html/classvtkFollower.html) is a subclass of `vtkActor` that automatically orients itself to always face the active camera. `SetCamera()` connects it to the renderer's camera. `SetScale()` and `AddPosition()` control size and placement. `GetProperty().SetColor()` sets the text color.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the axes and text polygon data to graphics primitives.
- [vtkVectorText](https://www.vtk.org/doc/nightly/html/classvtkVectorText.html) creates 3D polygon text from a string. `SetText("Origin")` specifies the label content.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data. `ResetCameraClippingRange()` adjusts near/far planes after positioning.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
