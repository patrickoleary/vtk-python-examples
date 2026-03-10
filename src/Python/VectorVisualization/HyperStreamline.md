### Description

This example visualizes tensor fields using hyperstreamlines seeded at four corner points of a simulated point load.

**PointLoad → HyperStreamline → Mapper → Actor | ImageDataGeometryFilter → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) indicates the point of load application.
- [vtkHyperStreamline](https://www.vtk.org/doc/nightly/html/classvtkHyperStreamline.html) integrates along an eigenvector to produce a tube-shaped streamline.
- [vtkImageDataGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkImageDataGeometryFilter.html) extracts a mid-plane slice for context.
- [vtkLogLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLogLookupTable.html) maps scalar stress values to color logarithmically.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a bounding box outline.
- [vtkPointLoad](https://www.vtk.org/doc/nightly/html/classvtkPointLoad.html) generates a tensor field from a simulated point load.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
