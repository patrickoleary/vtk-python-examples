### Description

This example demonstrates vtkInteractorStyleRubberBandZoom, which allows the user to draw a rectangle to zoom into a region of the scene. A 5×5 grid of colored spheres provides visual context for the zoom operation.

**SphereSource (×25) → Mappers → Actors → Renderer → Window → Interactor (RubberBandZoom style)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkInteractorStyleRubberBandZoom](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleRubberBandZoom.html) maps a rubber-band rectangle to a camera zoom.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates spheres for the grid.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
