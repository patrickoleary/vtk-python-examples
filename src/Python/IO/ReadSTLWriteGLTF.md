### Description

This example reads an STL mesh, renders it, and exports the scene to a glTF (.gltf) file.

**STL Reader → Mapper → Actor → Renderer → Window → GLTF Exporter → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with front and back face colors.
- [vtkGLTFExporter](https://www.vtk.org/doc/nightly/html/classvtkGLTFExporter.html) exports the entire render window scene to a glTF 2.0 (.gltf) file. `InlineDataOn()` embeds geometry data directly in the JSON file. glTF is a royalty-free format widely used for 3D content on the web, in AR/VR, and in game engines.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkSTLReader](https://www.vtk.org/doc/nightly/html/classvtkSTLReader.html) reads a stereolithography (.stl) file. `SetFileName()` specifies the input mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
