### Description

This example samples a quadric implicit function on a volume grid and extracts multiple iso-surfaces at different values using vtkContourFilter, rendered with semi-transparency.

**Quadric → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetOpacity()` makes the nested surfaces semi-transparent.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts three iso-surfaces using `GenerateValues()` to create evenly spaced contour levels between -0.5 and 0.5.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the iso-surfaces to graphics primitives. `SetScalarRange()` controls the color-mapping range.
- [vtkQuadric](https://www.vtk.org/doc/nightly/html/classvtkQuadric.html) defines an ellipsoidal implicit function via its 10 coefficients.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the quadric on a 50x50x50 volume grid within specified bounds.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
