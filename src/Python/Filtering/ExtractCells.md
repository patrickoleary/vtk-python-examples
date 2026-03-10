### Description

This example demonstrates vtkExtractCells to extract every other cell from a sphere mesh, creating a checkerboard pattern highlighted over a wireframe context.

**SphereSource → ExtractCells → DataSetSurfaceFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetSurfaceFilter](https://www.vtk.org/doc/nightly/html/classvtkDataSetSurfaceFilter.html) converts the unstructured grid output back to polydata.
- [vtkExtractCells](https://www.vtk.org/doc/nightly/html/classvtkExtractCells.html) extracts a subset of cells by their IDs from any dataset.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the extracted and context geometry to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the input sphere mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
