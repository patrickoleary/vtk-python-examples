### Description

This example worlds point picking using vtkWorldPointPicker. Left-click anywhere in the scene to get the world XYZ coordinates at that pixel depth (from the z-buffer). A yellow sphere marker is placed at the picked location. Unlike vtkCellPicker or vtkPointPicker, vtkWorldPointPicker does not require intersection with geometry — it reads directly from the depth buffer, making it very fast.

**Multiple sources → Mappers → Actors + vtkWorldPointPicker → marker sphere at picked position**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates cone geometry.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates cube geometry.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates cylinder geometry.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) base class for the custom interactor.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polydata to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere geometry.
- [vtkWorldPointPicker](https://www.vtk.org/doc/nightly/html/classvtkWorldPointPicker.html) reads the z-buffer to determine world coordinates at any pixel.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
