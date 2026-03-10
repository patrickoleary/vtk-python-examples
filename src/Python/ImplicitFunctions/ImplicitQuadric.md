### Description

This example visualizes an implicit quadric surface (ellipsoid) by sampling it on a volume grid using vtkSampleFunction and extracting the zero isosurface with vtkContourFilter. The quadric coefficients produce an elongated ellipsoidal shape rendered in alice blue with steel blue edges. It follows the VTK pipeline structure:

**Quadric → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry with `EdgeVisibilityOn()` to show the mesh wireframe.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface — the ellipsoidal surface.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkQuadric](https://www.vtk.org/doc/nightly/html/classvtkQuadric.html) defines an implicit quadric function via `SetCoefficients()`. The ten coefficients specify the general second-order equation F(x,y,z) = a0·x² + a1·y² + a2·z² + a3·xy + a4·yz + a5·xz + a6·x + a7·y + a8·z + a9 = 0.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit quadric on a regular 40×40×40 grid over [−0.5, 0.5]³.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
