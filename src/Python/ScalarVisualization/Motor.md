### Description

This example textures clipping of a motor model using a transparent texture map.

**BYUReader → PolyDataNormals → ImplicitTextureCoords → DataSetMapper → Actor (+ Texture) → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkBYUReader](https://www.vtk.org/doc/nightly/html/classvtkBYUReader.html) reads the motor geometry parts.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) configures the viewpoint.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the textured geometry to graphics primitives.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkImplicitTextureCoords](https://www.vtk.org/doc/nightly/html/classvtkImplicitTextureCoords.html) generates texture coordinates from the implicit function.
- [vtkPlanes](https://www.vtk.org/doc/nightly/html/classvtkPlanes.html) defines the cutting planes for texture clipping.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes surface normals.
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) reads the texture map.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the transparent texture map.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
