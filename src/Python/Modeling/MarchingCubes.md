### Description

This example extracts an isosurface from a voxelized sphere using vtkFlyingEdges3D. A sphere source is voxelized with vtkVoxelModeller and the isosurface is extracted at value 0.5. It follows the VTK pipeline structure:

**SphereSource → VoxelModeller → FlyingEdges3D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays the isosurface in misty rose.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts an isosurface at value 0.5 with computed normals.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) represents a regular image or volume.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the isosurface to graphics primitives.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere with 20-sided resolution.
- [vtkVoxelModeller](https://www.vtk.org/doc/nightly/html/classvtkVoxelModeller.html) converts the sphere surface into a 50³ voxel volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
