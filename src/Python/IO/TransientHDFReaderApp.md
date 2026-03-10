### Description

This example reads transient data from a VTK HDF file and animates through the time steps using a repeating timer callback.

**Reader → Mapper → Actor → Renderer → Window → Interactor + Timer Animation**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines a diverging blue-white-red color map via `SetColorSpaceToDiverging()` and `AddRGBPoint()` control points.
- [vtkCompositePolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkCompositePolyDataMapper.html) maps composite (multi-block) polydata to graphics primitives. `SelectColorArray()` and `SetScalarModeToUsePointFieldData()` color the surface by a named field.
- [vtkHDFReader](https://www.vtk.org/doc/nightly/html/classvtkHDFReader.html) reads a VTK HDF (.vtkhdf) file containing time-varying data. `SetFileName()` specifies the input file. `SetStep()` selects the time step and `GetNumberOfSteps()` reports the total count.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) maps mouse motion to camera transformations.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `UseHiddenLineRemovalOn()` improves wireframe rendering of overlapping surfaces.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events. `CreateRepeatingTimer()` drives the animation; an `AnimationCallback` observer advances the time step on each timer event.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
