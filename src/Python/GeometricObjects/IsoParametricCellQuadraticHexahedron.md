### Description

This example renders a single quadratic hexahedron isoparametric cell using [vtkQuadraticHexahedron](https://www.vtk.org/doc/nightly/html/classvtkQuadraticHexahedron.html). The 3D cell is rotated for viewing, centered at the origin, and displayed with vertex-ordering labels, gold sphere glyphs, and a translucent plinth.

**Cell → UnstructuredGrid → DataSetMapper → Actor + Glyphs + Labels → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) renders 2D overlay geometry.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) creates a translucent plinth beneath the cell.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the grid to graphics primitives.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places gold sphere glyphs at each vertex.
- [vtkLabeledDataMapper](https://www.vtk.org/doc/nightly/html/classvtkLabeledDataMapper.html) displays vertex-ordering labels.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkQuadraticHexahedron](https://www.vtk.org/doc/nightly/html/classvtkQuadraticHexahedron.html) defines the cell geometry.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) defines text appearance (font, color, size).
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformFilter.html) rotates the cell for 3D viewing.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the cell.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.