### Description

This example thises interactive demo renders a quadratic hexahedron with a slider widget that controls the chord error of vtkTessellatorFilter. Drag the slider to see the tessellation edges update in real time. It follows the VTK pipeline structure:

**Data → Filter → Mapper → Actor → Renderer → Window → Interactor → Widget**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. The tessellated cell actor uses `EdgeVisibilityOn()` to show subdivision edges. The glyph actor highlights node positions.
- [vtkCommand](https://www.vtk.org/doc/nightly/html/classvtkCommand.html) provides command functionality.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the tessellated cell and glyphs to graphics primitives.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places small [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) glyphs at each node position.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) provides minimal standard random sequence functionality.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkQuadraticHexahedron](https://www.vtk.org/doc/nightly/html/classvtkQuadraticHexahedron.html) defines a 20-node quadratic hexahedral cell with perturbed nodes.
- [vtkSliderRepresentation2D](https://www.vtk.org/doc/nightly/html/classvtkSliderRepresentation2D.html) 2D slider representation.
- [vtkSliderWidget](https://www.vtk.org/doc/nightly/html/classvtkSliderWidget.html) with [vtkSliderRepresentation2D](https://www.vtk.org/doc/nightly/html/classvtkSliderRepresentation2D.html) provides interactive chord error control.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkTessellatorFilter](https://www.vtk.org/doc/nightly/html/classvtkTessellatorFilter.html) subdivides the quadratic cell into linear elements. `SetChordError()` controls the tessellation accuracy. Edge visibility is enabled so the mesh density is visible.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) represents unstructured geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a slate gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
