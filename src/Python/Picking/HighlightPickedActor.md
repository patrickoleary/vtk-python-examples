### Description

This example highlights a picked actor by changing its color. Left-click on a sphere to highlight it in red with visible edges; the previous highlight is automatically restored. Ten randomly positioned and colored spheres are generated procedurally. A custom interactor style subclasses vtkInteractorStyleTrackballCamera to override left-button press handling with vtkPropPicker.

**vtkSphereSource → vtkPolyDataMapper → Actor + vtkPropPicker → highlight via property change**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) base class for the custom interactor.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random positions and colors.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polydata to graphics primitives.
- [vtkPropPicker](https://www.vtk.org/doc/nightly/html/classvtkPropPicker.html) performs hardware-accelerated prop picking.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) stores and restores actor appearance properties.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
