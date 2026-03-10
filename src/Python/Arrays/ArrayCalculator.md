### Description

This example uses vtkArrayCalculator to derive a new scalar array from point coordinates, then warps a plane by the computed values and visualizes the result with scalar coloring. The expression `sin(pi*x) * cos(pi*y)` produces a radial sinusoidal pattern.

**Plane → Elevation → Array Calculator → Warp Scalar → Lookup Table → Mapper → Actor → Scalar Bar → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Scalar coloring from the calculator output drives the surface appearance.
- [vtkArrayCalculator](https://www.vtk.org/doc/nightly/html/classvtkArrayCalculator.html) derives a new scalar array using a mathematical expression. `AddCoordinateScalarVariable()` exposes X and Y coordinates as variables. `SetFunction()` defines the expression. `SetResultArrayName()` names the output array.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) creates an initial scalar field from the diagonal direction.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to a diverging blue-to-red color ramp.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates a high-resolution planar mesh.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the warped polygon data to graphics primitives. `SetScalarModeToUsePointFieldData()` and `SelectColorArray()` select the computed array for coloring.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the color legend.
- [vtkWarpScalar](https://www.vtk.org/doc/nightly/html/classvtkWarpScalar.html) displaces the plane along its normal by the computed scalar values. `SetScaleFactor()` controls the warp amplitude.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data. `GetActiveCamera().Elevation()` and `Azimuth()` rotate the initial viewpoint.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
