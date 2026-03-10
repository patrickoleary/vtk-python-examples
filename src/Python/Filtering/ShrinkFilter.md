### Description

This example shrinks the cells of a sphere toward their centroids using vtkShrinkPolyData, revealing the individual polygonal faces with gaps between them.

**SphereSource → ShrinkPolyData → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` outlines each shrunk face.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the shrunk polydata to graphics primitives.
- [vtkShrinkPolyData](https://www.vtk.org/doc/nightly/html/classvtkShrinkPolyData.html) moves each cell's points toward the cell centroid by a configurable shrink factor (0.5 = 50% shrink), creating visible gaps between adjacent faces.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a 30x30 resolution sphere providing many faces for the shrink effect.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
