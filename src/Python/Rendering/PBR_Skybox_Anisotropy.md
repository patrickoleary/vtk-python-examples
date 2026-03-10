### Description

This example renders Boy's parametric surface with anisotropic PBR texturing and an HDR skybox backdrop. Carbon-fibre albedo, normal, ORM, and anisotropy-angle textures are applied. The environment map provides image-based lighting.

**Source → Tangents → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with PBR anisotropic texture properties.
- [vtkHDRReader](https://www.vtk.org/doc/nightly/html/classvtkHDRReader.html) loads the HDR equirectangular environment map.
- [vtkOpenGLRenderer](https://www.vtk.org/doc/nightly/html/classvtkOpenGLRenderer.html) provides the PBR-capable renderer with environment lighting.
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) loads the carbon-fibre albedo, ORM, normal, and anisotropy-angle PNG textures.
- [vtkParametricBoy](https://www.vtk.org/doc/nightly/html/classvtkParametricBoy.html) defines Boy's parametric surface equation.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the parametric function into polygon data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface polygon data to graphics primitives.
- [vtkPolyDataTangents](https://www.vtk.org/doc/nightly/html/classvtkPolyDataTangents.html) computes tangent vectors for anisotropic PBR shading.
- [vtkSkybox](https://www.vtk.org/doc/nightly/html/classvtkSkybox.html) renders the environment map as the scene backdrop.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) holds the HDR environment and PBR material textures.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
