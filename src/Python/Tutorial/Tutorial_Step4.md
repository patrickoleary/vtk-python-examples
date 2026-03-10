### Description

This example creates multiple actors with different surface properties and transformations, demonstrating two ways to control actor appearance.

**ConeSource → PolyDataMapper → Actor1 (inline property) + Actor2 (shared property) → Renderer → RenderWindow**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) orchestrates rendering; two instances share the same mapper.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a polygonal cone.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) controls surface appearance (color, diffuse, specular); can be shared across actors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) a viewport that draws its actors.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
