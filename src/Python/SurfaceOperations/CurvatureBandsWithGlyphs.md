### Description

This example gaussians curvature banded contours with normal glyphs on a parametric RandomHills surface. Custom bands partition the curvature into regions showing planar, hyperbolic (saddle), and spherical geometry. Edge curvatures are adjusted using weighted-average smoothing.

**ParametricFunctionSource → Curvatures → BandedPolyDataContourFilter → Mapper → Actor | MaskPoints → Glyph3D → Mapper → Actor | ScalarBarActor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkArrowSource](https://www.vtk.org/doc/nightly/html/classvtkArrowSource.html) generates the arrow glyph shape.
- [vtkBandedPolyDataContourFilter](https://www.vtk.org/doc/nightly/html/classvtkBandedPolyDataContourFilter.html) partitions the curvature into indexed contour bands.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) provides the Brewer Qualitative Set3 color scheme.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) maps scalar values to colors via piecewise interpolation.
- [vtkCurvatures](https://www.vtk.org/doc/nightly/html/classvtkCurvatures.html) computes Gaussian curvature at each surface point.
- [vtkFeatureEdges](https://www.vtk.org/doc/nightly/html/classvtkFeatureEdges.html) extracts boundary edges for curvature adjustment.
- [vtkGenerateIds](https://www.vtk.org/doc/nightly/html/classvtkGenerateIds.html) assigns point IDs for boundary edge detection.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places oriented arrow glyphs along surface normals.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) stores lists of VTK ids.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps curvature band indices and elevation scalars to colors.
- [vtkMaskPoints](https://www.vtk.org/doc/nightly/html/classvtkMaskPoints.html) subsamples surface points for glyphing.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the parametric surface with Z-based scalars.
- [vtkParametricRandomHills](https://www.vtk.org/doc/nightly/html/classvtkParametricRandomHills.html) defines the parametric random hills surface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays curvature and elevation legends.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) rotates the surface so Y is up.
- [vtkVariant](https://www.vtk.org/doc/nightly/html/classvtkVariant.html) provides variant functionality.
- [vtkVariantArray](https://www.vtk.org/doc/nightly/html/classvtkVariantArray.html) provides variant array functionality.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
