### Description

This example clips a superquadric with a plane using vtkClipPolyData and applies a back-face property so the interior appears solid. The retained half shows a tomato back-face color, while the clipped-away portion is displayed as a faint translucent ghost. It follows the VTK pipeline structure:

**SuperquadricSource → ClipPolyData (with vtkPlane) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the retained half with back-face coloring, and the clipped ghost at 10% opacity.
- [vtkClipPolyData](https://www.vtk.org/doc/nightly/html/classvtkClipPolyData.html) removes geometry on the positive side of the plane. `GenerateClippedOutputOn()` keeps the removed portion available.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit clip function — a diagonal plane through the origin.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the retained and clipped surfaces to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) creates a back-face property with flat tomato color (ambient only, no diffuse or specular).
- [vtkSuperquadricSource](https://www.vtk.org/doc/nightly/html/classvtkSuperquadricSource.html) generates a superquadric surface with configurable phi and theta roundness.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
