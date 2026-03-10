### Description

This example displays sixteen linear cell types in a single renderer arranged in a 4 × 4 grid. Each cell shows its vertex-ordering numbers as labels and gold sphere glyphs at the vertices. Three-dimensional cells sit on a translucent plinth.

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Each cell has a surface actor with `EdgeVisibilityOn()`, a glyph actor for vertex spheres, and optionally a translucent plinth actor with `SetOpacity()`.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) displays the vertex-index labels for each cell.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) creates a translucent plinth beneath 3D cells.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps each unstructured grid to graphics primitives.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places gold [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) glyphs at the vertices.
- [vtkHexagonalPrism](https://www.vtk.org/doc/nightly/html/classvtkHexagonalPrism.html) provides hexagonal prism functionality.
- [vtkHexahedron](https://www.vtk.org/doc/nightly/html/classvtkHexahedron.html) provides hexahedron functionality.
- [vtkLabeledDataMapper](https://www.vtk.org/doc/nightly/html/classvtkLabeledDataMapper.html) displays point-index labels.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) provides line functionality.
- [vtkPentagonalPrism](https://www.vtk.org/doc/nightly/html/classvtkPentagonalPrism.html) provides pentagonal prism functionality.
- [vtkPixel](https://www.vtk.org/doc/nightly/html/classvtkPixel.html) provides pixel functionality.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyLine](https://www.vtk.org/doc/nightly/html/classvtkPolyLine.html) provides poly line functionality.
- [vtkPolyVertex](https://www.vtk.org/doc/nightly/html/classvtkPolyVertex.html) provides poly vertex functionality.
- [vtkPolygon](https://www.vtk.org/doc/nightly/html/classvtkPolygon.html) provides polygon functionality.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkPyramid](https://www.vtk.org/doc/nightly/html/classvtkPyramid.html) provides pyramid functionality.
- [vtkQuad](https://www.vtk.org/doc/nightly/html/classvtkQuad.html) provides quad functionality.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkTetra](https://www.vtk.org/doc/nightly/html/classvtkTetra.html) provides tetra functionality.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) displays the cell type name as a 2D title pinned to the bottom of each viewport.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) defines text appearance (font, color, size).
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformFilter.html) rotates 3D cells so their depth is visible from the straight-on view.
- [vtkTriangle](https://www.vtk.org/doc/nightly/html/classvtkTriangle.html) provides triangle functionality.
- [vtkTriangleStrip](https://www.vtk.org/doc/nightly/html/classvtkTriangleStrip.html) provides triangle strip functionality.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) represents unstructured geometry.
- [vtkVertex](https://www.vtk.org/doc/nightly/html/classvtkVertex.html) provides vertex functionality.
- [vtkVoxel](https://www.vtk.org/doc/nightly/html/classvtkVoxel.html) provides voxel functionality.
- [vtkWedge](https://www.vtk.org/doc/nightly/html/classvtkWedge.html) provides wedge functionality.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
