### Description

This example imports a 3DS scene file and renders it with a gradient background. Unlike the standard VTK pipeline, an importer handles reading, filtering, mapping, and actor creation in a single step:

**Importer → Renderer → Window → Interactor**

- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) positions and orients the view. `SetPosition()`, `SetFocalPoint()`, and `SetViewUp()` define the camera frame; `Azimuth()` and `Elevation()` adjust the viewing angle.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `SetBackground()` and `SetBackground2()` with `GradientBackgroundOn()` create a gradient background. `ResetCamera()` reframes after import since the importer adds actors the renderer did not know about at creation time.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
