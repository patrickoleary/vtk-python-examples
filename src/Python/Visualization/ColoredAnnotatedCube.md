### Description

This example colors the individual faces of an annotated cube and display it as an orientation widget.

**Source → Transform → Elevation → BandedContours → Mapper → Actor → Renderer → Window → Interactor → Widgets**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAnnotatedCubeActor](https://www.vtk.org/doc/nightly/html/classvtkAnnotatedCubeActor.html) creates a cube with labeled faces.
- [vtkAxesActor](https://www.vtk.org/doc/nightly/html/classvtkAxesActor.html) draws labeled X, Y, and Z axes.
- [vtkBandedPolyDataContourFilter](https://www.vtk.org/doc/nightly/html/classvtkBandedPolyDataContourFilter.html) partitions the elevation into colored bands.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) provides a spectral color scheme.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates cone polygon data.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a unit cube with per-face colors.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) computes scalar values based on height.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors.
- [vtkOrientationMarkerWidget](https://www.vtk.org/doc/nightly/html/classvtkOrientationMarkerWidget.html) displays the orientation markers in the viewport.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPropAssembly](https://www.vtk.org/doc/nightly/html/classvtkPropAssembly.html) combines the annotated cube and colored cube.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines the scaling transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies the transform to the cone.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) stores per-face RGB colors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
