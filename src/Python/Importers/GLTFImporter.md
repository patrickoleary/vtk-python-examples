### Description

This example imports a glTF scene file and renders it with a gradient background. Unlike the standard VTK pipeline, an importer handles reading, filtering, mapping, and actor creation in a single step:

**Importer → Renderer → Window → Interactor**

- [vtkGLTFImporter](https://www.vtk.org/doc/nightly/html/classvtkGLTFImporter.html) reads a glTF 2.0 (.gltf) file and populates the render window with actors, cameras, and lights. `SetFileName()` specifies the input file. glTF is a royalty-free format widely used for 3D content on the web, in AR/VR, and in game engines.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `SetBackground()` and `SetBackground2()` with `GradientBackgroundOn()` create a gradient background. `ResetCamera()` reframes after import since the importer adds actors the renderer did not know about at creation time.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
