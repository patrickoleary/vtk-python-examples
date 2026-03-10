### Description

This example visualizes a procedural swirling vector field as a hedgehog plot on a structured grid.

**StructuredGrid (procedural) → HedgeHog → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkHedgeHog](https://www.vtk.org/doc/nightly/html/classvtkHedgeHog.html) draws a line segment at each point oriented along the vector.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates a bounding outline.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkStructuredGrid.html) holds the procedural 15×15×15 grid with vectors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
