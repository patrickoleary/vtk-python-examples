### Description

This example clips a sphere with a plane and caps the open boundary by converting the boundary edge loop into a filled polygon. After clipping with vtkClipPolyData, vtkFeatureEdges extracts the boundary loop and vtkStripper joins the edges into a continuous polyline whose lines are reinterpreted as polygon faces. It follows the VTK pipeline structure:

**SphereSource → ClipPolyData (with vtkPlane) → FeatureEdges → Stripper → Cap Polygon → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the clipped surface and the cap polygon.
- [vtkClipPolyData](https://www.vtk.org/doc/nightly/html/classvtkClipPolyData.html) removes the portion of the sphere on the positive side of the plane.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the clipped surface with flat shading and visible edges in tomato red.
- [vtkFeatureEdges](https://www.vtk.org/doc/nightly/html/classvtkFeatureEdges.html) extracts boundary edges from the clipped surface — the open edge loop where the cap will go.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines a diagonal clip plane through the sphere center.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cap polygon in banana yellow.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a tessellated sphere with 20×11 resolution.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) joins boundary edges into continuous polylines. The polyline points and lines are then reinterpreted as polygon vertices and faces to form the cap.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
