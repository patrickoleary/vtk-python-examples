### Description

This example cuts an outer sphere using a boolean texture map to reveal an inner sphere. Two implicit planes generate texture coordinates via vtkImplicitTextureCoords, and a boolean texture map makes portions of the outer sphere transparent where the implicit function is "inside."

**SphereSource → ImplicitTextureCoords + BooleanTexture → DataSetMapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry and texture.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the textured dataset to graphics primitives.
- [vtkDoubleArray](https://www.vtk.org/doc/nightly/html/classvtkDoubleArray.html) stores the plane normal vectors.
- [vtkImplicitTextureCoords](https://www.vtk.org/doc/nightly/html/classvtkImplicitTextureCoords.html) generates texture coordinates using implicit functions.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlanes](https://www.vtk.org/doc/nightly/html/classvtkPlanes.html) defines the implicit planes used for texture coordinate generation.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores the plane origin points.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the inner sphere to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the inner and outer sphere geometry.
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) reads the boolean texture map.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the boolean texture to the outer sphere.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
