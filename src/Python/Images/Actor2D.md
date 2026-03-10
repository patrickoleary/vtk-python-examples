### Description

This example renders 2D points in display coordinates using vtkActor2D and vtkPolyDataMapper2D. Three points are placed along the diagonal of the window and displayed as gold dots. It follows the VTK pipeline structure:

**Points → PolyData → VertexGlyphFilter → PolyDataMapper2D → Actor2D → Renderer → Window → Interactor**

- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) displays the 2D geometry with configurable color and point size.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) and [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) define three points in display coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper2D](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper2D.html) maps 2D polygon data to graphics primitives.
- [vtkVertexGlyphFilter](https://www.vtk.org/doc/nightly/html/classvtkVertexGlyphFilter.html) converts the points to vertex cells so they can be rendered.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
