### Description

This example demonstrates per-block coloring of a vtkMultiBlockDataSet using vtkCompositePolyDataMapper with per-block display attributes. Two spheres are assembled into a multiblock dataset with one intentionally NULL block, then rendered with distinct colors per block.

**Sources → Multi-Block → Composite Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the composite mapper to the scene. Per-block colors are set on the mapper rather than the actor.
- [vtkCompositeDataDisplayAttributes](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataDisplayAttributes.html) stores per-block color, opacity, and visibility attributes.
- [vtkCompositePolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkCompositePolyDataMapper.html) renders all blocks in a composite dataset. `SetBlockColor()` assigns colors using flat indices (0=root, 1..N=blocks).
- [vtkMultiBlockDataSet](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockDataSet.html) assembles multiple datasets into a hierarchical composite structure. `SetBlock()` assigns datasets by index. NULL blocks are valid and handled by composite-aware algorithms.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates sphere polygon meshes at different positions and sizes.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
