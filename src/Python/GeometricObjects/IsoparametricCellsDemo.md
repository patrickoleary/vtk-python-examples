### Description

This example displays sixteen isoparametric (quadratic and higher-order) cell types in a 4 × 4 grid of viewports. Each cell shows its vertex-ordering numbers as labels and gold sphere glyphs at the vertices. Three-dimensional cells sit on a translucent plinth.

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to each viewport. Each cell has a surface actor with `EdgeVisibilityOn()`, a glyph actor for vertex spheres, and optionally a translucent plinth actor with `SetOpacity()`.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) displays the vertex-index labels in each viewport.
- [vtkBiQuadraticQuad](https://www.vtk.org/doc/nightly/html/classvtkBiQuadraticQuad.html) provides bi quadratic quad functionality.
- [vtkBiQuadraticQuadraticHexahedron](https://www.vtk.org/doc/nightly/html/classvtkBiQuadraticQuadraticHexahedron.html) provides bi quadratic quadratic hexahedron functionality.
- [vtkBiQuadraticQuadraticWedge](https://www.vtk.org/doc/nightly/html/classvtkBiQuadraticQuadraticWedge.html) provides bi quadratic quadratic wedge functionality.
- [vtkBiQuadraticTriangle](https://www.vtk.org/doc/nightly/html/classvtkBiQuadraticTriangle.html) provides bi quadratic triangle functionality.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) creates a translucent plinth beneath 3D cells.
- [vtkCubicLine](https://www.vtk.org/doc/nightly/html/classvtkCubicLine.html) provides cubic line functionality.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps each unstructured grid to graphics primitives.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places gold [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) glyphs at the vertices.
- [vtkLabeledDataMapper](https://www.vtk.org/doc/nightly/html/classvtkLabeledDataMapper.html) displays point-index labels.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkQuadraticEdge](https://www.vtk.org/doc/nightly/html/classvtkQuadraticEdge.html) provides quadratic edge functionality.
- [vtkQuadraticHexahedron](https://www.vtk.org/doc/nightly/html/classvtkQuadraticHexahedron.html) provides quadratic hexahedron functionality.
- [vtkQuadraticLinearQuad](https://www.vtk.org/doc/nightly/html/classvtkQuadraticLinearQuad.html) provides quadratic linear quad functionality.
- [vtkQuadraticLinearWedge](https://www.vtk.org/doc/nightly/html/classvtkQuadraticLinearWedge.html) provides quadratic linear wedge functionality.
- [vtkQuadraticPolygon](https://www.vtk.org/doc/nightly/html/classvtkQuadraticPolygon.html) explicitly defined points.
- [vtkQuadraticPyramid](https://www.vtk.org/doc/nightly/html/classvtkQuadraticPyramid.html) provides quadratic pyramid functionality.
- [vtkQuadraticQuad](https://www.vtk.org/doc/nightly/html/classvtkQuadraticQuad.html) provides quadratic quad functionality.
- [vtkQuadraticTetra](https://www.vtk.org/doc/nightly/html/classvtkQuadraticTetra.html) provides quadratic tetra functionality.
- [vtkQuadraticTriangle](https://www.vtk.org/doc/nightly/html/classvtkQuadraticTriangle.html) provides quadratic triangle functionality.
- [vtkQuadraticWedge](https://www.vtk.org/doc/nightly/html/classvtkQuadraticWedge.html) provides quadratic wedge functionality.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays text in the viewport.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) defines text appearance (font, color, size).
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformFilter.html) provides transform filter functionality.
- [vtkTriQuadraticHexahedron](https://www.vtk.org/doc/nightly/html/classvtkTriQuadraticHexahedron.html) provides tri quadratic hexahedron functionality.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) represents unstructured geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) viewports are arranged in a 4 × 4 grid.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
