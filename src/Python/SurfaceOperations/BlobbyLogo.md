### Description

This example implicits modelling to create a blobby VTK logo from letter geometry. The three letters are combined, distance-field modelled, and contoured to produce a smooth blobby surface.

**Reader → AppendPolyData → ImplicitModeller → ContourFilter → PolyDataNormals → Mapper → Actor | TransformPolyDataFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkAppendPolyData](https://www.vtk.org/doc/nightly/html/classvtkAppendPolyData.html) combines the three letter meshes into one dataset.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an isosurface representing the blobby offset surface.
- [vtkImplicitModeller](https://www.vtk.org/doc/nightly/html/classvtkImplicitModeller.html) computes a distance field from the combined letter geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes surface normals for smooth shading.
- [vtkPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkPolyDataReader.html) loads the V, T and K letter geometry.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies a transform to position each letter overlay.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
