### Description

This example reads an EnSight Gold case file using vtkGenericEnSightReader and display the geometry with scalar coloring. A small EnSight Gold dataset (a quad surface with a sinusoidal height scalar) is generated if the files do not already exist.

**Reader → DataSetSurfaceFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetSurfaceFilter](https://www.vtk.org/doc/nightly/html/classvtkDataSetSurfaceFilter.html) extracts surface geometry from the dataset.
- [vtkGenericEnSightReader](https://www.vtk.org/doc/nightly/html/classvtkGenericEnSightReader.html) reads EnSight Gold and EnSight 6 case files.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
