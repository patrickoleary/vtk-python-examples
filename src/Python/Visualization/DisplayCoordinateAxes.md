### Description

This example displays an interactive orientation marker with coordinate axes in the viewport.

**Source → Mapper → Actor → Renderer → Window → Interactor → Widget**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAxesActor](https://www.vtk.org/doc/nightly/html/classvtkAxesActor.html) draws labeled X, Y, and Z axes.
- [vtkOrientationMarkerWidget](https://www.vtk.org/doc/nightly/html/classvtkOrientationMarkerWidget.html) places the axes actor as an interactive orientation marker.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere polygon data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
