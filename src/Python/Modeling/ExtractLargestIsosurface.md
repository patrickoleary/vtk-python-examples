### Description

This example reads a structured points brain volume, extracts an isosurface with vtkFlyingEdges3D, and keeps only the largest connected region using vtkPolyDataConnectivityFilter. The brain surface is rendered with a skin color and a lighter backface property. It follows the VTK pipeline structure:

**StructuredPointsReader → FlyingEdges3D → PolyDataConnectivityFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the brain surface with a skin color front face and a lighter backface property.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts an isosurface at threshold 50 with computed normals and gradients.
- [vtkPolyDataConnectivityFilter](https://www.vtk.org/doc/nightly/html/classvtkPolyDataConnectivityFilter.html) retains only the largest connected region, removing small disconnected fragments.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the largest isosurface to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) loads the brain.vtk structured points volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
