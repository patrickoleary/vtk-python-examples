### Description

This example generates evenly spaced 2D streamlines from a procedural vector field using vtkEvenlySpacedStreamlines2D. A rotating vortex velocity field is defined on a uniform grid, and the filter produces streamlines that are evenly distributed across the domain. It follows the VTK pipeline structure:

**ImageData (vector field) → EvenlySpacedStreamlines2D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with `SetLineWidth(2)` for visibility.
- [vtkEvenlySpacedStreamlines2D](https://www.vtk.org/doc/nightly/html/classvtkEvenlySpacedStreamlines2D.html) generates streamlines that are evenly spaced across the 2D domain. `SetStartPosition()` seeds the first streamline, `SetSeparatingDistance(0.3)` controls the minimum spacing, and `SetIntegratorTypeToRungeKutta4()` selects the integration method.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) holds the 2D uniform grid with the procedural vortex vector field.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera with parallel projection for the 2D view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
