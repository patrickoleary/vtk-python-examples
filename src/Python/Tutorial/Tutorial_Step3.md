### Description

This example uses multiple renderers within a single render window to display two simultaneous views of the same cone, offset by 90 degrees.

**ConeSource → PolyDataMapper → Actor → Renderer (left) + Renderer (right) → RenderWindow**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) orchestrates rendering; shared between both renderers.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a polygonal cone.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) a viewport that draws its actors; two instances split the window.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
