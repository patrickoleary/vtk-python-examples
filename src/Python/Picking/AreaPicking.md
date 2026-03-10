### Description

This example areas picking with rubber-band selection using vtkAreaPicker. Press 'r' to enter rubber-band selection mode, then drag a rectangle to select actors within the region. Selected actors are highlighted in red. Twenty randomly positioned and colored spheres are generated procedurally. An EndPickEvent callback on the area picker iterates through the selected props and changes their color.

**vtkSphereSource (×20) → Mappers → Actors + vtkAreaPicker + vtkInteractorStyleRubberBandPick → highlight selected**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAreaPicker](https://www.vtk.org/doc/nightly/html/classvtkAreaPicker.html) selects actors within a rectangular screen region.
- [vtkInteractorStyleRubberBandPick](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleRubberBandPick.html) provides rubber-band rectangle drawing for area selection.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random positions and colors.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polydata to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
