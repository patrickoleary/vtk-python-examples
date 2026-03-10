### Description

This example evaluates the signed distance from a sphere surface on a regular 3-D grid using vtkImplicitPolyDataDistance and colour the grid points accordingly.

**Source → ImplicitPolyDataDistance → VertexGlyphFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores the signed distance values for each sample point.
- [vtkImplicitPolyDataDistance](https://www.vtk.org/doc/nightly/html/classvtkImplicitPolyDataDistance.html) computes signed distance from sample points to the sphere surface.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) defines the regular grid of sample points.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the sample point geometry and distance scalars.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the distance-coloured points to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the reference sphere polydata.
- [vtkVertexGlyphFilter](https://www.vtk.org/doc/nightly/html/classvtkVertexGlyphFilter.html) converts the sample points into renderable vertex cells.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
