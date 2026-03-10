### Description

This example deforms a sphere using vtkDeformPointSet with an octahedral control mesh. One control point is displaced upward, stretching the sphere into a teardrop shape. The sphere is colored by elevation using vtkElevationFilter. It follows the VTK pipeline structure:

**SphereSource → ElevationFilter → DeformPointSet (with control mesh) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the deformed sphere colored by elevation, and the control mesh as a black wireframe.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkDeformPointSet](https://www.vtk.org/doc/nightly/html/classvtkDeformPointSet.html) deforms the elevation-colored sphere using an octahedral control mesh. Moving a control point displaces the underlying surface smoothly.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) colors the sphere by height (z value) using a scalar field mapped between low and high points.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps both the deformed surface and the wireframe control mesh to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere with 51×17 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
