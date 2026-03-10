### Description

This example reads an SLC volume file, extracts an isosurface using the marching cubes algorithm, and renders it using the standard VTK pipeline.

**Reader → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an isosurface from the volume at a given scalar value using the marching cubes algorithm. `SetValue(0, iso_value)` sets the contour threshold.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the extracted surface to graphics primitives.
- [vtkSLCReader](https://www.vtk.org/doc/nightly/html/classvtkSLCReader.html) reads an SLC (.slc) volume file. `SetFileName()` specifies the input file. SLC is a simple volumetric format used for CT and MRI data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
