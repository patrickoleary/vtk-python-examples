### Description

This example interpolates a scalar field from scattered random points onto a sphere surface using vtkPointInterpolator with a Gaussian kernel. The scattered source points are shown as Gaussian splats alongside the smoothly interpolated surface. It follows the VTK pipeline structure:

**Random Points → PointInterpolator (with GaussianKernel) → ResampleWithDataSet (onto SphereSource) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the interpolated surface and the source point splats.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkGaussianKernel](https://www.vtk.org/doc/nightly/html/classvtkGaussianKernel.html) provides smooth radial-basis interpolation with configurable sharpness and radius.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) defines a 51³ volume enclosing the probe surface for interpolation.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates 200 reproducible random points inside a unit cube, each with a scalar value equal to its distance from the origin.
- [vtkPointGaussianMapper](https://www.vtk.org/doc/nightly/html/classvtkPointGaussianMapper.html) renders the source points as soft Gaussian splats with a custom shader.
- [vtkPointInterpolator](https://www.vtk.org/doc/nightly/html/classvtkPointInterpolator.html) interpolates source point scalars onto the volume grid using the Gaussian kernel.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the interpolated surface to graphics primitives.
- [vtkResampleWithDataSet](https://www.vtk.org/doc/nightly/html/classvtkResampleWithDataSet.html) projects the interpolated volume scalars onto the sphere probe surface.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere as the probe surface.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
