### Description

This example decimations of a laser-digitized face mesh compared side-by-side with the original.

**Reader → DecimatePro → PolyDataNormals → Mapper → Actor | Reader → PolyDataNormals → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) shared between both viewports for synchronized viewing.
- [vtkDecimatePro](https://www.vtk.org/doc/nightly/html/classvtkDecimatePro.html) reduces the mesh by 90% while preserving topology.
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) loads the face texture image.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes surface normals for smooth shading.
- [vtkPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkPolyDataReader.html) loads the Cyberware laser-digitized face mesh.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the texture map to both actors.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) two viewports: left shows original, right shows decimated.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
