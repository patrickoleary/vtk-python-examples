### Description

This example builds a graph as a vtkUnstructuredGrid with vertex degree scalars, then render it. Vertices are colored by degree using a lookup table and drawn as sphere glyphs; edges are rendered as gray lines.

**vtkUnstructuredGrid (VTK_LINE cells) → vtkDataSetMapper (edges) + vtkGlyph3DMapper (vertex spheres colored by degree)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) renders the line cells (edges).
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places sphere glyphs at vertices.
- [vtkIntArray](https://www.vtk.org/doc/nightly/html/classvtkIntArray.html) stores the per-vertex degree scalar.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps degree values to colors.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) provides the glyph shape.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) stores the graph as points and line cells.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
