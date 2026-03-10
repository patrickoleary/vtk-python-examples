### Description

This example visualizes an implicit toroidal superquadric by sampling it on a volume grid using vtkSampleFunction and extracting the zero isosurface with vtkContourFilter. The superquadric has sharp edges controlled by low phi and theta roundness values, producing a blocky torus rendered in alice blue with steel blue edges. It follows the VTK pipeline structure:

**Superquadric → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry with `EdgeVisibilityOn()` to show the mesh wireframe.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface — the superquadric surface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit superquadric on a regular 60×60×60 grid over [−1, 1]³.
- [vtkSuperquadric](https://www.vtk.org/doc/nightly/html/classvtkSuperquadric.html) defines an implicit superquadric function. `SetPhiRoundness(0.3)` and `SetThetaRoundness(0.4)` sharpen the profile. `SetToroidal(1)` switches from an ellipsoidal to a toroidal shape. `SetThickness(0.33)` controls the tube radius relative to the torus radius.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
