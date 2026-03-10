### Description

This example visualizes carotid artery blood flow using cone glyphs oriented by velocity.

**StructuredPointsReader → ThresholdPoints → MaskPoints → Glyph3D (+ ConeSource) → Mapper → Actor | ContourFilter → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) provides the glyph shape.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) generates a speed isosurface for context.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places cone glyphs oriented and scaled by velocity.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to color.
- [vtkMaskPoints](https://www.vtk.org/doc/nightly/html/classvtkMaskPoints.html) subsamples points for glyph placement.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a bounding box outline.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) reads the carotid artery velocity field.
- [vtkThresholdPoints](https://www.vtk.org/doc/nightly/html/classvtkThresholdPoints.html) keeps only high-speed points.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
