### Description

This example visualizes stress tensors as ellipsoids using tensor glyphs with a Brewer color palette.

**PointLoad → TensorGlyph (+ SphereSource) → PolyDataNormals → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) builds a Brewer diverging spectral lookup table.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) indicates the point of load application.
- [vtkImageDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkImageDataGeometryFilter.html) extracts a plane for scalar range reference.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a bounding box outline.
- [vtkPointLoad](https://www.vtk.org/doc/nightly/html/classvtkPointLoad.html) generates a tensor field from a simulated point load.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes normals for smooth shading.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) provides the ellipsoid glyph shape.
- [vtkTensorGlyph](https://www.vtk.org/doc/nightly/html/classvtkTensorGlyph.html) orients and scales spheres into ellipsoids by the stress tensor.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
