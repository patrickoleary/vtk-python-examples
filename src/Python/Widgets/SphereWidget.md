### Description

This example uses an interactive sphere widget that can be repositioned and resized. The sphere center is printed on each interaction.

**SphereWidget → Renderer → Window → Interactor**

- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkSphereWidget](https://www.vtk.org/doc/nightly/html/classvtkSphereWidget.html) provides an interactive sphere that can be moved and resized.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
