### Description

This example gaussians splatting of a single oriented point with an isosurface extraction. A cone glyph indicates the normal direction.

**PolyData → GaussianSplatter → ContourFilter → Mapper → Actor | OutlineFilter → Mapper → Actor | ConeSource → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone glyph indicating the normal direction.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an isosurface from the splatted volume.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores double data arrays.
- [vtkGaussianSplatter](https://www.vtk.org/doc/nightly/html/classvtkGaussianSplatter.html) splats the point into a volume using an eccentric Gaussian distribution.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a bounding box outline of the sampling volume.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) defines a single point with an oriented normal and scalar value.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
