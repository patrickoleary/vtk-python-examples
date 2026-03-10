### Description

This example adds an observer to the rendering pipeline. This extends Tutorial_Step1 by introducing the **command/observer design pattern** used throughout VTK.

**ConeSource → PolyDataMapper → Actor → Renderer (with observer) → RenderWindow**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) orchestrates rendering and holds surface properties.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a polygonal cone.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) a viewport that draws its actors; fires `StartEvent` before each render.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
