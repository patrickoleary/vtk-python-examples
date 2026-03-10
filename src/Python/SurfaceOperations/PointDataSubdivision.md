### Description

This example points data subdivision comparison: original, linear, and butterfly on a Boy surface. Three viewports show the original parametric surface, the result of vtkLinearSubdivisionFilter, and the result of vtkButterflySubdivisionFilter, each with arrow glyphs along surface normals.

**ParametricFunctionSource → SubdivisionFilter → Mapper → Actor | MaskPoints → Glyph3D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) renders 2D overlay geometry.
- [vtkArrowSource](https://www.vtk.org/doc/nightly/html/classvtkArrowSource.html) generates the arrow glyph shape.
- [vtkButterflySubdivisionFilter](https://www.vtk.org/doc/nightly/html/classvtkButterflySubdivisionFilter.html) applies butterfly subdivision to smooth the surface.
- [vtkColor3ub](https://www.vtk.org/doc/nightly/html/classvtkColor3ub.html) provides color3ub functionality.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) provides the Brewer Qualitative Set3 color scheme.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines a diverging green-to-red color map for elevation.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps unstructured data to graphics primitives.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places oriented arrow glyphs along surface normals.
- [vtkLinearSubdivisionFilter](https://www.vtk.org/doc/nightly/html/classvtkLinearSubdivisionFilter.html) applies linear subdivision to refine the surface.
- [vtkMaskPoints](https://www.vtk.org/doc/nightly/html/classvtkMaskPoints.html) subsamples surface points for glyphing.
- [vtkParametricBoy](https://www.vtk.org/doc/nightly/html/classvtkParametricBoy.html) defines the Boy parametric surface.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the parametric surface with Z-based scalars.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkTextMapper](https://www.vtk.org/doc/nightly/html/classvtkTextMapper.html) provides text mapper functionality.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) defines text appearance (font, color, size).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) three viewports: original, linear subdivision, butterfly subdivision.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
