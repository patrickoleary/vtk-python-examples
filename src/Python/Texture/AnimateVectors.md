### Description

This example animates vector field motion using texture map animation on the carotid artery dataset.

**StructuredPointsReader → ThresholdPoints → Glyph3D (LineSource) → PolyDataMapper + TextureMaps → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry and animated texture.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) positions the viewpoint.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places line glyphs at each thresholded point.
- [vtkLineSource](https://www.vtk.org/doc/nightly/html/classvtkLineSource.html) generates the line segment used as the glyph shape.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates a wireframe bounding box for context.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the glyphs and outline to graphics primitives.
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) reads the carotid artery dataset and the animation texture maps.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies each animation frame as a texture map.
- [vtkThresholdPoints](https://www.vtk.org/doc/nightly/html/classvtkThresholdPoints.html) filters points by scalar threshold.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
