### Description

This example renders five rows of PBR spheres demonstrating coat material properties. Columns vary coat strength or roughness; rows show different base materials. An HDR equirectangular environment map provides image-based lighting with a skybox.

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with varying PBR coat properties.
- [vtkHDRReader](https://www.vtk.org/doc/nightly/html/classvtkHDRReader.html) loads the HDR equirectangular environment map.
- [vtkOpenGLRenderer](https://www.vtk.org/doc/nightly/html/classvtkOpenGLRenderer.html) provides the PBR-capable renderer with environment lighting.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the sphere polygon data to graphics primitives.
- [vtkSkybox](https://www.vtk.org/doc/nightly/html/classvtkSkybox.html) renders the environment map as the scene backdrop.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere polygon data.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) holds the HDR environment texture.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
