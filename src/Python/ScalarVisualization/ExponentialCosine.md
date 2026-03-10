### Description

This example warps a plane with an exponential cosine function and color by derivative.

**PlaneSource → Transform → Compute → WarpScalar → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the warped surface to graphics primitives.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores double data arrays.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates a high-resolution plane.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) scales the plane to the desired domain.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies the transform to the plane.
- [vtkWarpScalar](https://www.vtk.org/doc/nightly/html/classvtkWarpScalar.html) warps the plane by the computed function values.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
