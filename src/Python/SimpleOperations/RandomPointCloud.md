### Description

This example generates and visualizes a random 3D point cloud using vtkMath random number generators. 500 points are sampled from a Gaussian (normal) distribution centered at the origin, creating a spherical cloud that is denser near the center.

**vtkMath → Points + Colors → PolyData → Mapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry and point size.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) defines each point as a vertex cell for rendering.
- [vtkMath](https://www.vtk.org/doc/nightly/html/classvtkMath.html) generates Gaussian-distributed random numbers for point positions.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the point cloud geometry and color data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the point cloud to graphics primitives.
- [vtkUnsignedCharArray](https://www.vtk.org/doc/nightly/html/classvtkUnsignedCharArray.html) stores per-point RGB colors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
