### Description

This example visualizes stress tensors as scaled and oriented principal axes using tensor glyphs.

**PointLoad → TensorGlyph (+ Axes) → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAxes](https://www.vtk.org/doc/nightly/html/classvtkAxes.html) provides the axes geometry for tensor glyphs.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) indicates the point of load application.
- [vtkImageDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkImageDataGeometryFilter.html) extracts a plane for scalar range reference.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar stress values to color with logarithmic scaling.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a bounding box outline.
- [vtkPointLoad](https://www.vtk.org/doc/nightly/html/classvtkPointLoad.html) generates a tensor field from a simulated point load.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkTensorGlyph](https://www.vtk.org/doc/nightly/html/classvtkTensorGlyph.html) orients and scales axes by the stress tensor.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
