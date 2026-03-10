### Description

This example demonstrates fixed text in the corners of the viewport using vtkCornerAnnotation, overlaid on a simple 3D scene. Corner annotations are commonly used in medical imaging viewers to display patient information, slice numbers, and window/level values.

**Source → Mapper → Actor → Corner Annotation → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the sphere color.
- [vtkCornerAnnotation](https://www.vtk.org/doc/nightly/html/classvtkCornerAnnotation.html) displays fixed text in the four corners of the viewport. `SetText(index, string)` sets text for each corner (0=lower-left, 1=lower-right, 2=upper-left, 3=upper-right). `SetLinearFontScaleFactor()` and `SetNonlinearFontScaleFactor()` control how the font scales with the window size.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere polygon mesh as background geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
