### Description

This example demonstrates Gaussian and Mean curvature on two surfaces (superquadric torus and RandomHills) in a 2×2 grid with a diverging colour map and scalar bars.

**Source → Curvatures → EdgeAdjustment → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) displays viewport title text.
- [vtkCleanPolyData](https://www.vtk.org/doc/nightly/html/classvtkCleanPolyData.html) merges duplicate points in the superquadric mesh.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) builds a diverging cool-to-warm colour ramp.
- [vtkCurvatures](https://www.vtk.org/doc/nightly/html/classvtkCurvatures.html) computes Gaussian and Mean curvature at each vertex.
- [vtkFeatureEdges](https://www.vtk.org/doc/nightly/html/classvtkFeatureEdges.html) extracts boundary edges to identify points needing curvature adjustment.
- [vtkGenerateIds](https://www.vtk.org/doc/nightly/html/classvtkGenerateIds.html) assigns original point IDs so boundary points can be mapped back after edge extraction.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) stores neighbour point IDs during edge curvature adjustment.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar curvature values to colours.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the parametric surface into polygons.
- [vtkParametricRandomHills](https://www.vtk.org/doc/nightly/html/classvtkParametricRandomHills.html) defines the RandomHills parametric surface function.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the curvature-coloured mesh to graphics primitives.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the curvature legend.
- [vtkSuperquadricSource](https://www.vtk.org/doc/nightly/html/classvtkSuperquadricSource.html) generates a superquadric torus surface.
- [vtkTextMapper](https://www.vtk.org/doc/nightly/html/classvtkTextMapper.html) renders viewport title strings.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) controls font, size, and alignment of viewport titles.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) scales the surface for better visualization.
- [vtkTransformFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformFilter.html) applies the scaling transform to the surface.
- [vtkTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkTriangleFilter.html) converts polygons to triangles for curvature computation.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
