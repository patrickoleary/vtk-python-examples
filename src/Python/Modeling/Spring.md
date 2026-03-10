### Description

This example creates a spring by rotationally extruding a circular cross-section with translation and delta-radius using vtkRotationalExtrusionFilter. The extrusion sweeps six full revolutions to form a helix, and vtkPolyDataNormals provides smooth shading. It follows the VTK pipeline structure:

**Cross-Section Points → PolyData → RotationalExtrusionFilter → PolyDataNormals → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the spring in powder blue with specular highlights and backface culling.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) and [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) define an 8-point circular cross-section for the spring wire.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the spring surface to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes normals with a 60° feature angle for smooth shading.
- [vtkRotationalExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkRotationalExtrusionFilter.html) sweeps the cross-section 2160° (six turns) with translation and radius change to form the helical spring.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
