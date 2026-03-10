### Description

This example visualizes all built-in VTK color series as rows of colored bars. Each row represents one color scheme from vtkColorSeries, with each bar showing one color in the scheme. This provides a visual catalog of the Brewer, categorical, and custom color palettes available in VTK.

**vtkColorSeries → PolyData (quads with cell colors) → Mapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) defines the quad cell connectivity.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) enumerates built-in color schemes (Brewer, categorical, custom).
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the quad corner coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the grid geometry and color data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the colored quads to graphics primitives.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) stores per-cell RGB color values.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
