### Description

This example subdivides a single tetrahedron into twelve smaller tetrahedra using vtkSubdivideTetra. The left viewport shows the original tetrahedron and the right viewport shows the subdivided result. Both are displayed with shrunk cells (via vtkShrinkFilter) and edge visibility so the internal structure is clearly visible. It follows the VTK pipeline structure:

**UnstructuredGrid → SubdivideTetra → ShrinkFilter → DataSetMapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show original and subdivided meshes with `EdgeVisibilityOn()`.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps unstructured grid data to graphics primitives.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) shrinks each cell toward its centroid with `SetShrinkFactor(0.8)` so individual tetrahedra are visible.
- [vtkSubdivideTetra](https://www.vtk.org/doc/nightly/html/classvtkSubdivideTetra.html) subdivides each tetrahedron by adding edge midpoints and a body center, producing twelve smaller tetrahedra per input cell. This is useful for mesh refinement of tetrahedral grids.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the input tetrahedron built from four points and one `VTK_TETRA` cell.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout. Cameras are shared so both viewports rotate together.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
