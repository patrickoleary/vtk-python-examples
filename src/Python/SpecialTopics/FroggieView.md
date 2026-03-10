### Description

This example views preprocessed VTK tissue surfaces of a segmented frog dataset with interactive opacity sliders. Loading is much faster than `FroggieSurface` because surfaces are read from pre-computed `.vtk` files.

**PolyDataReader → TransformPolyData → Normals → Mapper → Actor → Renderer → Window → Interactor (with SliderWidgets)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCameraOrientationWidget](https://www.vtk.org/doc/nightly/html/classvtkCameraOrientationWidget.html) provides an interactive orientation gizmo.
- [vtkCommand](https://www.vtk.org/doc/nightly/html/classvtkCommand.html) provides command functionality.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) maps mouse motion to camera transformations.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors.
- [vtkMatrix4x4](https://www.vtk.org/doc/nightly/html/classvtkMatrix4x4.html) orientation transforms keyed by acquisition order name.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) recomputes normals after the transform.
- [vtkPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkPolyDataReader.html) loads preprocessed tissue surfaces from VTK legacy files.
- [vtkSliderRepresentation2D](https://www.vtk.org/doc/nightly/html/classvtkSliderRepresentation2D.html) 2D slider representation.
- [vtkSliderWidget](https://www.vtk.org/doc/nightly/html/classvtkSliderWidget.html) provides per-tissue opacity controls.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) orients tissue surfaces according to slice acquisition order.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
