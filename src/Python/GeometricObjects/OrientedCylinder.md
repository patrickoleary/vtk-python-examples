### Description

This example orients a cylinder so it spans from one random 3D point to another, with spheres marking each endpoint. It follows the VTK pipeline structure:

**Source → Transform → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates a cylinder whose height vector is +y by default.
- [vtkMath](https://www.vtk.org/doc/nightly/html/classvtkMath.html) provides mathematical utility functions.
- [vtkMatrix4x4](https://www.vtk.org/doc/nightly/html/classvtkMatrix4x4.html) provides matrix4x4 functionality.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) generates reproducible random start and end points.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each element to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) marks the start (yellow) and end (magenta) points.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) combines translation, rotation (via the direction cosine matrix), a −90° z-rotation to swap the cylinder's +y height axis to +x, scaling to match the distance, and a half-unit y-shift so the base sits at the start point.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark blue background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
