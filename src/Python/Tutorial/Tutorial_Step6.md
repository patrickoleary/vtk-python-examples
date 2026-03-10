### Description

This example introduces 3D widgets with a vtkBoxWidget that interactively transforms the cone actor.

**ConeSource → PolyDataMapper → Actor → Renderer → RenderWindow → Interactor + BoxWidget**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) orchestrates rendering and holds surface properties.
- [vtkBoxWidget](https://www.vtk.org/doc/nightly/html/classvtkBoxWidget.html) a 3D widget for interactively transforming an actor via its bounding box.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a polygonal cone.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) provides trackball-style camera navigation.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) holds the transformation matrix applied to the actor by the widget callback.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) a viewport that draws its actors.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
