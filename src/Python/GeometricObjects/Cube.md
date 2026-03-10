### Description

This example manually constructs a cube as vtkPolyData — defining vertices, quad faces, and per-vertex scalars — and renders it with scalar color mapping. It follows the standard VTK pipeline structure:

**Data → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the mapped geometry.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) positions the view at (1, 1, 1) looking at the origin.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) holds the 6 quad faces, each defined by 4 vertex indices via [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html).
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) provides one scalar value per vertex, assigned via `GetPointData().SetScalars()` for color mapping.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) stores lists of VTK ids.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 8 vertices of a unit cube via `InsertPoint()`.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) assembles the points, polygons, and scalars into a single dataset.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives. `SetScalarRange()` controls the color mapping range.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a cornsilk background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
