### Description

This example stocks data visualization with closing price (top) and volume (bottom) views. Each stock curve is rendered as a tube with a text follower label.

**Reader → TubeFilter → TransformPolyDataFilter → Mapper → Actor | VectorText → Mapper → Follower → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkFollower](https://www.vtk.org/doc/nightly/html/classvtkFollower.html) orients text labels to always face the camera.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkPolyDataReader.html) loads stock data curves for GE, GM, IBM and DEC.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) positions and scales each stock in the scene.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) renders each stock curve as a tube.
- [vtkVectorText](https://www.vtk.org/doc/nightly/html/classvtkVectorText.html) generates text labels for each stock name.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) two viewports: top shows closing price, bottom shows volume from above.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
