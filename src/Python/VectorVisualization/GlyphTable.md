### Description

This example uses a glyph table to vary glyph shape by scalar value.

**RTAnalyticSource → ImageGradient → ElevationFilter → Glyph3D (+ CubeSource, SphereSource, ConeSource) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) provides a third glyph shape.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) provides one glyph shape.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) adds a smoothly varying scalar for glyph indexing.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) selects the glyph shape from a table indexed by scalar value.
- [vtkImageGradient](https://www.vtk.org/doc/nightly/html/classvtkImageGradient.html) computes the gradient to produce a vector attribute.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRTAnalyticSource](https://www.vtk.org/doc/nightly/html/classvtkRTAnalyticSource.html) generates a test wavelet image dataset.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) provides another glyph shape.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
