### Description

This example samples an implicit superquadric function on a volume grid using vtkSampleFunction and extracts an isosurface with vtkContourFilter. A bounding box outline shows the sampling volume. The superquadric has rounded phi and sharp theta parameters, producing a pillow-like shape. It follows the VTK pipeline structure:

**Superquadric → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the isosurface at value 2.0. `GenerateValues(1, 2.0, 2.0)` creates a single contour at that value.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) creates a wireframe bounding box around the sampling volume for spatial context.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface and outline to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit function on a regular 50×50×50 grid over [−2, 2]³, producing a scalar volume.
- [vtkSuperquadric](https://www.vtk.org/doc/nightly/html/classvtkSuperquadric.html) defines an implicit superquadric function. `SetPhiRoundness(2.5)` and `SetThetaRoundness(0.5)` control the shape — higher phi roundness produces a more rounded profile while lower theta roundness sharpens the equatorial cross-section.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
