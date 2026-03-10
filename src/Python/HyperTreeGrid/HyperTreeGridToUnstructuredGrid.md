### Description

This example converts a hyper tree grid to an unstructured grid using vtkHyperTreeGridToUnstructuredGrid and renders both side by side. The left viewport shows the original HTG surface colored by Depth with edge visibility. The right viewport shows the converted unstructured grid with shrunk cells (via vtkShrinkFilter) so individual hexahedra are visible. It follows the VTK pipeline structure:

**Source → HyperTreeGridGeometry → Mapper → Actor (left) | Source → ToUnstructuredGrid → ShrinkFilter → DataSetMapper → Actor (right)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the HTG surface and the shrunk unstructured grid.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the unstructured grid data to graphics primitives.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of the HTG as polydata for the left viewport.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field.
- [vtkHyperTreeGridToUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridToUnstructuredGrid.html) converts a hyper tree grid into a standard vtkUnstructuredGrid. Each leaf cell becomes a hexahedral cell, making the data compatible with general VTK filters that do not support HTG natively.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the HTG surface polydata to graphics primitives.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) shrinks each cell toward its centroid with `SetShrinkFactor(0.8)` so individual cells are visible.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a side-by-side layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
