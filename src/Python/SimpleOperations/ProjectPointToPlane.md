### Description

This example visualizes the projection of a 3D point onto a plane. A red sphere marks the original point, a green sphere marks the projected point, and a yellow line shows the perpendicular projection. A cyan arrow indicates the plane normal direction. The semi-transparent blue quad represents the plane.

**PlaneSource + SphereSource (×2) + ArrowSource + Line + VectorText (×3) → Mapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkArrowSource](https://www.vtk.org/doc/nightly/html/classvtkArrowSource.html) generates the plane normal arrow.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) defines the line cell connectivity.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) computes the point projection onto the plane.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates the visible plane geometry.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the projection line endpoints.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the line geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygonal data into graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates spheres marking the original and projected points.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) orients and scales the normal arrow.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies the transform to the arrow geometry.
- [vtkVectorText](https://www.vtk.org/doc/nightly/html/classvtkVectorText.html) generates 3D text labels.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
