### Description

This example demonstrates vtkGradientFilter to compute gradient vectors of a Gaussian scalar field on a structured grid, then visualizes them as arrow glyphs.

**StructuredGrid → GradientFilter → Glyph3D (arrows) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkArrowSource](https://www.vtk.org/doc/nightly/html/classvtkArrowSource.html) generates the arrow glyph shape.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places arrow glyphs oriented along the gradient vectors.
- [vtkGradientFilter](https://www.vtk.org/doc/nightly/html/classvtkGradientFilter.html) computes the gradient of a scalar field, producing a vector field.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the output to graphics primitives.
- [vtkStructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkStructuredGrid.html) holds the procedural grid with a Gaussian height field.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts surface geometry for the scalar-colored base.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
