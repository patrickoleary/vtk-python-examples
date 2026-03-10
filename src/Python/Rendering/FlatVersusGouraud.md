### Description

This example compares flat versus Gouraud shading on four different geometries: sphere, cylinder, isosurface, and an OBJ model (cow). Top row uses flat shading; bottom row uses Gouraud shading. Linked cameras let you rotate each pair together.

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with flat or Gouraud interpolation.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an isosurface from the sampled quadric volume.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates the cylinder polygon data.
- [vtkOBJReader](https://www.vtk.org/doc/nightly/html/classvtkOBJReader.html) loads the cow model from an `.obj` file.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkQuadric](https://www.vtk.org/doc/nightly/html/classvtkQuadric.html) defines the implicit quadric function for the isosurface.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the quadric function on a regular grid to produce a volume.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere polygon data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
