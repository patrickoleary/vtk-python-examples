### Description

This example generates a synthetic swirling vector field on a 3D volume grid and traces streamlines through it using vtkStreamTracer, displayed as gold tubes.

**ImageData (vector field) → PointSource (seeds) → StreamTracer → TubeFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the tube color.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) holds a 30x30x30 volume grid with a procedurally generated swirling vector field.
- [vtkPointSource](https://www.vtk.org/doc/nightly/html/classvtkPointSource.html) generates 50 random seed points near the bottom of the field.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the streamline tubes to graphics primitives. `ScalarVisibilityOff()` disables color-mapping so the actor color is used.
- [vtkStreamTracer](https://www.vtk.org/doc/nightly/html/classvtkStreamTracer.html) integrates the vector field forward from each seed point, producing streamline polylines.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) wraps tubes around the streamlines for 3D visibility.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
