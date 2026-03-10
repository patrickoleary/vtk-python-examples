### Description

This example aligns a source point set to a target point set using vtkIterativeClosestPointTransform (ICP) with a rigid body transform, and visualizes the source (red), target (green), and transformed result (blue) as colored sphere glyphs.

**Source Points + Target Points → ICP Transform → TransformPolyDataFilter → Glyph3DMappers → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Three actors are used — red for source, green for target, blue for the transformed result.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places sphere glyphs at each point for visualization of the three point sets.
- [vtkIterativeClosestPointTransform](https://www.vtk.org/doc/nightly/html/classvtkIterativeClosestPointTransform.html) computes a rigid body transform that minimizes the distance between source and target point sets.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the small sphere used as the glyph shape. `SetRadius()` controls the glyph size.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies the computed ICP transform to the source points.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera. `ResetCamera()` frames all three point sets.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
