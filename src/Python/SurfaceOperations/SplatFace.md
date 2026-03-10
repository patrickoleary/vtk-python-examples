### Description

This example ellipticals Gaussian splatting to reconstruct a face surface from oriented points. The original wireframe mesh is overlaid for comparison.

**Reader → PolyDataNormals → MaskPoints → GaussianSplatter → ContourFilter → Mapper → Actor | Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry. The original mesh is displayed as wireframe overlay.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an isosurface from the splatted volume.
- [vtkGaussianSplatter](https://www.vtk.org/doc/nightly/html/classvtkGaussianSplatter.html) splats oriented points into a 100³ volume with elliptical eccentricity.
- [vtkMaskPoints](https://www.vtk.org/doc/nightly/html/classvtkMaskPoints.html) subsamples every 8th point for splatting.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes surface normals for oriented splatting.
- [vtkPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkPolyDataReader.html) loads the Cyberware laser-digitized face mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
