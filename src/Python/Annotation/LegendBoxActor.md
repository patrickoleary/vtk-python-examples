### Description

This example demonstrates a legend box with colored symbols using vtkLegendBoxActor, showing labels for three geometric objects in the scene. The legend displays a small icon and text label for each entry.

**Sources → Mappers → Actors → Legend Box → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Three actors are created — one per object. `GetProperty().SetColor()` sets a distinct color for each (tomato, steel blue, gold).
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a cube.
- [vtkLegendBoxActor](https://www.vtk.org/doc/nightly/html/classvtkLegendBoxActor.html) displays a legend with labeled color swatches. `SetNumberOfEntries()` allocates legend slots. `SetEntry()` associates polydata, a label string, and a color with each slot. `UseBackgroundOn()` enables a semi-transparent background panel.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each object's polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html), [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html), and [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generate three geometric objects placed side by side.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
