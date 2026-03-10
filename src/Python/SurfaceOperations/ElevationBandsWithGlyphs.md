### Description

This example elevations banded contours with normal glyphs on a parametric RandomHills surface. The banded contour filter and an indexed lookup table partition the elevation into color bands, while arrow glyphs show surface normals colored by elevation.

**ParametricFunctionSource → BandedPolyDataContourFilter → Mapper → Actor | MaskPoints → Glyph3D → Mapper → Actor | ScalarBarActor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkArrowSource](https://www.vtk.org/doc/nightly/html/classvtkArrowSource.html) generates the arrow glyph shape.
- [vtkBandedPolyDataContourFilter](https://www.vtk.org/doc/nightly/html/classvtkBandedPolyDataContourFilter.html) partitions the elevation into indexed contour bands.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) provides the Brewer Qualitative Set3 color scheme.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places oriented arrow glyphs along surface normals.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps elevation band indices to colors.
- [vtkMaskPoints](https://www.vtk.org/doc/nightly/html/classvtkMaskPoints.html) subsamples surface points for glyphing.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the parametric surface with Z-based scalars.
- [vtkParametricRandomHills](https://www.vtk.org/doc/nightly/html/classvtkParametricRandomHills.html) defines the parametric random hills surface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the elevation legend.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) rotates the surface so Y is up.
- [vtkVariant](https://www.vtk.org/doc/nightly/html/classvtkVariant.html) provides variant functionality.
- [vtkVariantArray](https://www.vtk.org/doc/nightly/html/classvtkVariantArray.html) provides variant array functionality.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
