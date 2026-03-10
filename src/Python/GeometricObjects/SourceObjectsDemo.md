### Description

This example displays nine VTK source objects (Sphere, Cone, Cylinder, Cube, Plane, Text, PointSource, Disk, Line) arranged in a 3 × 3 grid inside a single renderer. Each object has a tomato back-face colour. It follows the VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) renders each object in peach puff with a tomato back-face, positioned on a 3-column grid with `SetPosition()`.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a cube.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates a cylinder.
- [vtkDiskSource](https://www.vtk.org/doc/nightly/html/classvtkDiskSource.html) generates a disk.
- [vtkLineSource](https://www.vtk.org/doc/nightly/html/classvtkLineSource.html) generates a line segment.
- [vtkPlaneSource](https://www.vtk.org/doc/nightly/html/classvtkPlaneSource.html) generates a plane.
- [vtkPointSource](https://www.vtk.org/doc/nightly/html/classvtkPointSource.html) generates random points in a sphere.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each source to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays text in the viewport.
- [vtkTextSource](https://www.vtk.org/doc/nightly/html/classvtkTextSource.html) generates polygonal text.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a blue-grey background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
