### Description

This example clips an unstructured grid with a diagonal plane (y+z normal) using vtkClipDataSet. The retained and clipped portions are displayed in orange and purple, rotated apart to expose the cut faces. Unlike vtkTableBasedClipDataSet, vtkClipDataSet does not retain original cells — hexahedra in unclipped regions are converted to tetrahedra.

**Reader → ClipDataSet → DataSetMapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkClipDataSet](https://www.vtk.org/doc/nightly/html/classvtkClipDataSet.html) clips the unstructured grid without retaining original cell types.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps any dataset type to graphics primitives.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit clipping plane.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) rotates each output half apart for visualization.
- [vtkUnstructuredGridReader](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGridReader.html) reads the treemesh unstructured grid dataset.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
