### Description

This example reads a Protein Data Bank (.pdb) file using vtkPDBReader and display the molecular structure as sphere glyphs colored by atom type. A small caffeine molecule PDB file is generated if it does not already exist.

**Reader → Glyph3DMapper (SphereSource) → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places a sphere glyph at each atom position.
- [vtkPDBReader](https://www.vtk.org/doc/nightly/html/classvtkPDBReader.html) reads Protein Data Bank molecular structure files.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the glyph geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
