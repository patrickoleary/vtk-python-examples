### Description

This example demonstrates 2D text annotation with single-line and multi-line text using various horizontal and vertical justification options. Alignment guide lines show the positioning coordinates.

**Text Properties → Text Mappers → Actor2Ds → Grid → Renderer → Window → Interactor**

- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) positions each text block in normalized display coordinates. `GetPositionCoordinate().SetValue()` places the text at a specific viewport location.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkCoordinate](https://www.vtk.org/doc/nightly/html/classvtkCoordinate.html) transforms grid line coordinates from normalized viewport to display space.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper2D](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper2D.html) renders the alignment guide lines as 2D overlay geometry.
- [vtkTextMapper](https://www.vtk.org/doc/nightly/html/classvtkTextMapper.html) creates 2D text from a string. `SetInput()` accepts newline characters for multi-line text. `GetTextProperty()` controls justification and color per mapper.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) defines font family, size, bold, italic, shadow, and line spacing. Two shared property objects are created — one for single-line labels (plain) and one for multi-line labels (bold italic with shadow).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the text actors and grid overlay into a single scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
