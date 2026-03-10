### Description

This example displays a cube slab on layer 0 and axes on layer 1, demonstrating layered rendering. Press '0' or '1' to switch the interactive layer; camera orientation is synchronised between layers after interaction.

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAxesActor](https://www.vtk.org/doc/nightly/html/classvtkAxesActor.html) renders labelled XYZ axes on layer 1.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates the cube slab on layer 0.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) provides trackball-style camera interaction.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cube polygon data to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) controls edge visibility and colour on the cube.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) configures the user transform on the axes actor.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. Two renderers on separate layers.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
