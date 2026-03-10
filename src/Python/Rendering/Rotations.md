### Description

This example demonstrates all four rotation sequences (X, Y, Z, then X+Y) of the cow model with EraseOff overlay, reproducing VTK Textbook figures 3-31a through 3-31d in a single run.

**Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAxes](https://www.vtk.org/doc/nightly/html/classvtkAxes.html) generates XYZ reference axes.
- [vtkBYUReader](https://www.vtk.org/doc/nightly/html/classvtkBYUReader.html) loads the cow model from a `.g` file.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cow and axes polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
