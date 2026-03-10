### Description

This example reads a VTK legacy unstructured grid (.vtk) file containing eleven linear cells and visualizes them with multiple techniques: shrunk cell faces, tube-wrapped edges, sphere glyphs at points, point ID labels, and a category legend.

**Reader → Filters → Mappers → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Three actors are used — shrunk cell faces with `EdgeVisibilityOn()`, tubed edges with specular highlights, and point sphere glyphs colored banana with specular shading.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) displays the point ID labels as 2D text overlays.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkCategoryLegend](https://www.vtk.org/doc/nightly/html/classvtkCategoryLegend.html) displays a legend mapping cell type names to colors.
- [vtkCellTypeUtilities](https://www.vtk.org/doc/nightly/html/classvtkCellTypeUtilities.html) provides cell type utilities functionality.
- [vtkContextTransform](https://www.vtk.org/doc/nightly/html/classvtkContextTransform.html) provides context transform functionality.
- [vtkContextView](https://www.vtk.org/doc/nightly/html/classvtkContextView.html) hosts the 2D category legend overlay alongside the 3D scene.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the shrunk cells to graphics primitives with per-cell coloring.
- [vtkExtractEdges](https://www.vtk.org/doc/nightly/html/classvtkExtractEdges.html) extracts the edges of all cells as line segments.
- [vtkGenericCell](https://www.vtk.org/doc/nightly/html/classvtkGenericCell.html) provides generic cell functionality.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places a sphere glyph at each point in the dataset.
- [vtkLabeledDataMapper](https://www.vtk.org/doc/nightly/html/classvtkLabeledDataMapper.html) displays point IDs as text labels at each point location.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) assigns a distinct color to each cell type. A deep copy with `IndexedLookupOn()` is used for the category legend.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) pulls each cell's faces toward its centroid, visually separating cells to reveal their individual shapes.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) wraps each edge line with a tube for visibility.
- [vtkUnstructuredGridReader](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGridReader.html) reads a VTK legacy unstructured grid (.vtk) file. `SetFileName()` specifies the input file.
- [vtkVariantArray](https://www.vtk.org/doc/nightly/html/classvtkVariantArray.html) provides variant array functionality.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
