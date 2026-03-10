### Description

This example estimates normals for a point cloud using vtkPCANormalEstimation and displays them as hedgehog glyphs. A procedural sphere point cloud is used as input and the estimated normals are shown as short lines from each point. It follows the VTK pipeline structure:

**PointCloud → PCANormalEstimation → HedgeHog → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the point cloud and the normal hedgehog glyphs.
- [vtkHedgeHog](https://www.vtk.org/doc/nightly/html/classvtkHedgeHog.html) creates a line from each point along its normal vector. `SetScaleFactor(0.1)` controls the line length.
- [vtkPCANormalEstimation](https://www.vtk.org/doc/nightly/html/classvtkPCANormalEstimation.html) estimates point normals using local PCA (principal component analysis). `SetSampleSize(20)` sets the local neighborhood size and `SetNormalOrientationToGraphTraversal()` ensures consistent normal orientation.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
