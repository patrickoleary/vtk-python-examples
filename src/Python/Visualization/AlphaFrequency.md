### Description

This example linearlies extrude letter glyphs to visualize character frequency in a text file.

**Source → Extrude → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkLinearExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkLinearExtrusionFilter.html) extrudes each letter proportionally to its frequency.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkVectorText](https://www.vtk.org/doc/nightly/html/classvtkVectorText.html) generates 3D vector text polygon data for each letter.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
