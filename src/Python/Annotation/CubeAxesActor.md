### Description

This example demonstrates labeled axes around the bounding box of a 3D object using vtkCubeAxesActor. The axes show tick marks, labels, and titles for each coordinate direction.

**Source → Mapper → Actor → Cube Axes → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `GetProperty().SetColor()` sets the superquadric color.
- [vtkCubeAxesActor](https://www.vtk.org/doc/nightly/html/classvtkCubeAxesActor.html) draws labeled axes around a bounding box. `SetBounds()` defines the box extent. `SetCamera()` connects the axes to the active camera for proper orientation. `SetFlyModeToStaticTriad()` keeps three axes visible. `GetTitleTextProperty()` and `GetLabelTextProperty()` control axis title and label appearance.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkSuperquadricSource](https://www.vtk.org/doc/nightly/html/classvtkSuperquadricSource.html) generates a superquadric shape. `SetPhiRoundness()` and `SetThetaRoundness()` control the shape's curvature.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data. `GetActiveCamera().Azimuth()` and `Elevation()` rotate the initial viewpoint.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
