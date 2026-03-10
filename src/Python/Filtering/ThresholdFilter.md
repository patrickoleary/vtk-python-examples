### Description

This example generates a sphere with elevation scalars along the Y axis, then extracts only the cells within a middle elevation band using vtkThreshold, colored by the elevation values.

**SphereSource → ElevationFilter → Threshold → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` outlines each cell in the thresholded band.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the thresholded unstructured grid to graphics primitives. `SetScalarRange()` controls the color-mapping range.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) computes a scalar value for each point based on its projection onto a line between low and high reference points.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkThreshold](https://www.vtk.org/doc/nightly/html/classvtkThreshold.html) extracts cells whose scalar values fall within a specified range (0.3–0.7), effectively keeping a horizontal band around the equator.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
