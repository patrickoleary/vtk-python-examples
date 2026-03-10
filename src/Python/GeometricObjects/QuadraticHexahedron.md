### Description

This example renders a quadratic hexahedron with tessellation and node glyphs. It follows the VTK pipeline structure:

**Data → Filter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties — tomato diffuse color with black edges for the hex, banana for the node glyphs.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps both the tessellated cell and glyphs to graphics primitives.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places small [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) glyphs at each node position.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) provides minimal standard random sequence functionality.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkQuadraticHexahedron](https://www.vtk.org/doc/nightly/html/classvtkQuadraticHexahedron.html) defines a 20-node quadratic hexahedral cell. Parametric coordinates are perturbed with [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) for visual interest.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkTessellatorFilter](https://www.vtk.org/doc/nightly/html/classvtkTessellatorFilter.html) subdivides the quadratic cell into linear elements for rendering.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the quadratic cell and its points.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a slate gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
