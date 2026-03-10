### Description

This example constructs a Koch snowflake fractal using recursive edge subdivision, shown as an outline (left) and triangulated fill colored by iteration level (right).

**Points → recursive subdivision → PolyLine / Triangles → Mapper → Actor → Renderer × 2 → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores integer data arrays.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps iteration level to a blue saturation ramp.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the recursively generated curve vertices.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyLine](https://www.vtk.org/doc/nightly/html/classvtkPolyLine.html) connects the curve points into a closed outline.
- [vtkTriangle](https://www.vtk.org/doc/nightly/html/classvtkTriangle.html) fills the snowflake interior with recursive triangulation.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
