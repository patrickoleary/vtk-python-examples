### Description

This example dices a sphere into pieces using vtkOBBDicer, which partitions the mesh along oriented bounding box (OBB) splits. Each piece is colored differently using the piece index scalar assigned by the dicer. It follows the VTK pipeline structure:

**SphereSource → OBBDicer → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkOBBDicer](https://www.vtk.org/doc/nightly/html/classvtkOBBDicer.html) partitions the mesh into approximately 10 pieces by recursively splitting along the longest axis of the oriented bounding box. `SetDiceModeToSpecifiedNumberOfPieces()` targets the requested number.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the diced mesh to graphics primitives, coloring by the piece index scalar.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a high-resolution tessellated sphere with 40×40 resolution.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
