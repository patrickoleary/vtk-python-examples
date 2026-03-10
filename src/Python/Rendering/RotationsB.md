### Description

This example sixes incremental rotations of the cow model about the Y axis, rendered with EraseOff so all orientations overlap.

**Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAxes](https://www.vtk.org/doc/nightly/html/classvtkAxes.html) generates XYZ reference axes.
- [vtkBYUReader](https://www.vtk.org/doc/nightly/html/classvtkBYUReader.html) loads the cow model from a `.g` file.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cow and axes polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
