### Description

This example warps a flat structured grid by a procedural radial displacement vector field.

**StructuredGrid (procedural) → StructuredGridGeometryFilter → WarpVector → PolyDataNormals → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates a bounding outline.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) recomputes normals for smooth shading.
- [vtkStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkStructuredGrid.html) holds the procedural 30×30 flat grid with displacement vectors.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts the surface for rendering.
- [vtkWarpVector](https://www.vtk.org/doc/nightly/html/classvtkWarpVector.html) displaces points by the vector field.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
