### Description

This example computes Gaussian and Mean curvatures on a RandomHills parametric surface, adjust edge curvatures via distance-weighted averaging of interior neighbours, and display side-by-side with a cool-to-warm LUT.

**Source → Curvatures → EdgeAdjustment → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) displays viewport title text.
- [vtkCameraOrientationWidget](https://www.vtk.org/doc/nightly/html/classvtkCameraOrientationWidget.html) provides an interactive orientation gizmo.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) builds a diverging cool-to-warm colour ramp.
- [vtkCurvatures](https://www.vtk.org/doc/nightly/html/classvtkCurvatures.html) computes Gaussian and Mean curvature at each vertex.
- [vtkFeatureEdges](https://www.vtk.org/doc/nightly/html/classvtkFeatureEdges.html) extracts boundary edges to identify points needing curvature adjustment.
- [vtkGenerateIds](https://www.vtk.org/doc/nightly/html/classvtkGenerateIds.html) assigns original point IDs so boundary points can be mapped back after edge extraction.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) stores neighbour point IDs during edge curvature adjustment.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar curvature values to colours.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the parametric surface into polygons.
- [vtkParametricRandomHills](https://www.vtk.org/doc/nightly/html/classvtkParametricRandomHills.html) defines the parametric surface function.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the curvature-coloured mesh to graphics primitives.
- [vtkPolyDataTangents](https://www.vtk.org/doc/nightly/html/classvtkPolyDataTangents.html) computes tangent vectors on the surface.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the curvature legend.
- [vtkTextMapper](https://www.vtk.org/doc/nightly/html/classvtkTextMapper.html) renders viewport title strings.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) controls font, size, and alignment of viewport titles.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) scales the surface for better visualization.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies the scaling transform to the surface.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
