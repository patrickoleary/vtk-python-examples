### Description

This example thes cow 'walking' around the global origin by composing incremental rotations and translations, rendered with EraseOff overlay.

**Reader → Transform → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAxes](https://www.vtk.org/doc/nightly/html/classvtkAxes.html) generates XYZ reference axes.
- [vtkBYUReader](https://www.vtk.org/doc/nightly/html/classvtkBYUReader.html) loads the cow model from a `.g` file.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cow and axes polygon data to graphics primitives.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) composes incremental rotations and translations for the walk animation.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
