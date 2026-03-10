### Description

This example shows anatomical planes transecting a human figure with annotated orientation markers.

**Reader → Mapper → Actor | PlaneSource → Transform → Mapper → Actor | VectorText → Transform → Mapper → Actor | AnnotatedCube + Axes → OrientationWidget → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAnnotatedCubeActor](https://www.vtk.org/doc/nightly/html/classvtkAnnotatedCubeActor.html) displays an annotated cube with anatomical labels.
- [vtkAxesActor](https://www.vtk.org/doc/nightly/html/classvtkAxesActor.html) displays labeled coordinate axes.
- [vtkOrientationMarkerWidget](https://www.vtk.org/doc/nightly/html/classvtkOrientationMarkerWidget.html) places orientation markers in viewport corners.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates the anatomical plane geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPropAssembly](https://www.vtk.org/doc/nightly/html/classvtkPropAssembly.html) combines the axes and annotated cube.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) orients each plane and text label.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies transforms to polydata.
- [vtkVectorText](https://www.vtk.org/doc/nightly/html/classvtkVectorText.html) generates 3D text labels for the planes.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) reads the human figure model.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
