### Description

This example Blow-molding simulation showing ten time steps of parison deformation. The color indicates thickness: red is thinnest, blue is thickest.

**Reader → WarpVector → ConnectivityFilter → GeometryFilter → PolyDataNormals → Mapper → Actor | ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConnectivityFilter](https://www.vtk.org/doc/nightly/html/classvtkConnectivityFilter.html) extracts the parison region from the dataset.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the mold surface as a wireframe contour.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the mold wireframe to graphics primitives.
- [vtkDataSetReader](https://www.vtk.org/doc/nightly/html/classvtkDataSetReader.html) loads the blow-molding simulation data with displacement vectors.
- [vtkGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkGeometryFilter.html) converts the unstructured grid to polydata for normal computation.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps thickness scalars to a rainbow color scale.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes surface normals for smooth shading.
- [vtkWarpVector](https://www.vtk.org/doc/nightly/html/classvtkWarpVector.html) deforms the parison mesh by displacement vectors at each time step.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) ten viewports in a 2×5 grid, one per time step.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
