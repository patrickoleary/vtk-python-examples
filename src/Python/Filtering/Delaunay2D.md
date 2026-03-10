### Description

This example creates a terrain-like height field on a 10x10 grid and triangulates it with vtkDelaunay2D, displaying both the triangulated mesh with tube-style edges and the input points as spheres.

**Points → Delaunay2D + VertexGlyphFilter → Mappers → Actors → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. `EdgeVisibilityOn()` and `SetEdgeColor()` style the mesh edges; `SetPointSize()` and `RenderPointsAsSpheresOn()` style the point glyphs.
- [vtkDelaunay2D](https://www.vtk.org/doc/nightly/html/classvtkDelaunay2D.html) triangulates a set of 2D-projected points into a surface mesh.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the triangulated mesh and the vertex glyphs to graphics primitives.
- [vtkVertexGlyphFilter](https://www.vtk.org/doc/nightly/html/classvtkVertexGlyphFilter.html) converts bare points to renderable vertex cells displayed as deep pink spheres.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
