### Description

This example compares [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) and [vtkMarchingCubes](https://www.vtk.org/doc/nightly/html/classvtkMarchingCubes.html) side by side on a CT head dataset. Both algorithms extract the skin isosurface at contour value 500; the left viewport shows FlyingEdges3D and the right shows MarchingCubes. The two algorithms produce identical geometry but FlyingEdges3D is significantly faster on multi-core systems.

**Reader → FlyingEdges3D / MarchingCubes → Mappers → Actors → Left/Right Renderers → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts an isosurface using the parallel flying-edges algorithm.
- [vtkMarchingCubes](https://www.vtk.org/doc/nightly/html/classvtkMarchingCubes.html) extracts an isosurface using the classic marching cubes algorithm.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the MetaImage (.mhd/.raw) CT volume.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) controls skin and backface colors.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) displays algorithm labels in each viewport.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
