### Description

This example visualizes flow momentum by warping computational planes with the velocity vector.

**MultiBlockPLOT3DReader → StructuredGridGeometryFilter → AppendPolyData → WarpVector → PolyDataNormals → Mapper → Actor | StructuredGridOutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAppendPolyData](https://www.vtk.org/doc/nightly/html/classvtkAppendPolyData.html) merges the three planes into a single dataset.
- [vtkMultiBlockPLOT3DReader](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockPLOT3DReader.html) reads the combustor geometry and solution files.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) recomputes normals for smooth shading.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts computational planes at specific i-indices.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates a bounding outline.
- [vtkWarpVector](https://www.vtk.org/doc/nightly/html/classvtkWarpVector.html) displaces plane geometry by the momentum vector.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
