### Description

This example places different glyph shapes at each point using vtkProgrammableGlyphFilter.

**Points → ProgrammableGlyphFilter (+ ConeSource, CubeSource, SphereSource) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) provides one glyph shape.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) provides another glyph shape.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkProgrammableGlyphFilter](https://www.vtk.org/doc/nightly/html/classvtkProgrammableGlyphFilter.html) calls a user-defined callback to select the glyph source per point.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) provides a third glyph shape.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
