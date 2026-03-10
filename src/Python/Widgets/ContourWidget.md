### Description

This example draws an interactive contour initialized from a circle. The contour can be warped by dragging the control points.

**Points → PolyData → ContourWidget → Renderer → Window → Interactor**

- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkContourWidget](https://www.vtk.org/doc/nightly/html/classvtkContourWidget.html) provides interactive contour drawing and editing.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkOrientedGlyphContourRepresentation](https://www.vtk.org/doc/nightly/html/classvtkOrientedGlyphContourRepresentation.html) renders the contour with oriented glyph control points.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the initial circle point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the initial contour polyline.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
