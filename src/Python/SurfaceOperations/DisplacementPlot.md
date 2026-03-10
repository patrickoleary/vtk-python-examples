### Description

This example surfaces displacement plot of a vibrating plane colored by vector dot product. The second torsional mode is shown with a diverging color scheme: cool for negative motion, warm for positive, white at the nodes.

**Reader → WarpVector → PolyDataNormals → VectorDot → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines a diverging green-to-red color map.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the warped surface to graphics primitives.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps dot-product scalars to the diverging color scheme.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes surface normals on the warped geometry.
- [vtkPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkPolyDataReader.html) loads the plate vibration data with mode8 displacement vectors.
- [vtkVectorDot](https://www.vtk.org/doc/nightly/html/classvtkVectorDot.html) computes the dot product between normals and displacement vectors to produce modal scalars.
- [vtkWarpVector](https://www.vtk.org/doc/nightly/html/classvtkWarpVector.html) deforms the surface by displacement vectors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
