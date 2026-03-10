### Description

This example cuts a surface model using scalar-based contours.

**Reader → ScalarComputation → ContourFilter → Mapper → Actor | Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts contour lines from the scalar field.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores the computed scalar distances.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit plane for scalar evaluation.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) reads the polygonal surface model.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
