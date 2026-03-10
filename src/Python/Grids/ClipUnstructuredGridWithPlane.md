### Description

This example clips an unstructured grid with a vertical plane (x-axis normal) using vtkTableBasedClipDataSet. The retained and clipped portions are displayed in gold and steel blue, separated along the x-axis. Unlike other clipping filters, vtkTableBasedClipDataSet retains original cells if they are not clipped.

**Reader → TableBasedClipDataSet → DataSetMapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps any dataset type to graphics primitives.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit clipping plane.
- [vtkTableBasedClipDataSet](https://www.vtk.org/doc/nightly/html/classvtkTableBasedClipDataSet.html) clips the unstructured grid, retaining original unclipped cells.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) rotates each output half apart for visualization.
- [vtkUnstructuredGridReader](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGridReader.html) reads the treemesh unstructured grid dataset.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
