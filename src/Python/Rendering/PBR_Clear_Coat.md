### Description

This example renders a PBR cube with albedo, ORM, normal, and coat-normal texture maps demonstrating the clear-coat material layer. An HDR equirectangular environment map provides image-based lighting.

**Source → TriangleFilter → Tangents → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with PBR clear-coat properties.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates the cube polygon data.
- [vtkHDRReader](https://www.vtk.org/doc/nightly/html/classvtkHDRReader.html) loads the HDR equirectangular environment map.
- [vtkLight](https://www.vtk.org/doc/nightly/html/classvtkLight.html) provides a directional light for the scene.
- [vtkOpenGLRenderer](https://www.vtk.org/doc/nightly/html/classvtkOpenGLRenderer.html) provides the PBR-capable renderer with environment lighting.
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) loads the albedo, ORM, and normal PNG textures.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the cube polygon data to graphics primitives.
- [vtkPolyDataTangents](https://www.vtk.org/doc/nightly/html/classvtkPolyDataTangents.html) computes tangent vectors for normal mapping.
- [vtkSkybox](https://www.vtk.org/doc/nightly/html/classvtkSkybox.html) renders the environment map as the scene backdrop.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) holds the HDR environment and PBR material textures.
- [vtkTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkTriangleFilter.html) triangulates the cube faces for tangent generation.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
