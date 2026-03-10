### Description

This example visualizes the closest point on a line segment to a given query point. Blue spheres mark the line segment endpoints, a red sphere marks the query point, and a green sphere marks the computed closest point. A yellow perpendicular line connects the query point to the closest point, with the distance displayed as a label.

**SphereSource (×4) + Lines (×2) + VectorText (×3) → Mapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) defines the line cell connectivity.
- [vtkLine](https://www.vtk.org/doc/nightly/html/classvtkLine.html) computes the closest point on a line segment and the squared distance.
- [vtkMath](https://www.vtk.org/doc/nightly/html/classvtkMath.html) provides mathematical utility functions.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores line endpoint coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the line geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates spheres marking the query point, closest point, and line endpoints.
- [vtkVectorText](https://www.vtk.org/doc/nightly/html/classvtkVectorText.html) generates 3D text for distance and coordinate labels.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
