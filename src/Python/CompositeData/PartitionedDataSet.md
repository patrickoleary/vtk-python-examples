### Description

This example demonstrates vtkPartitionedDataSet by grouping four geometric objects (sphere, cube, cylinder, cone) as partitions and rendering them with per-partition coloring using a composite-aware mapper.

**Sources → Partitioned Dataset → Composite Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the composite mapper to the scene. Per-partition colors are set on the mapper rather than the actor.
- [vtkCompositeDataDisplayAttributes](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataDisplayAttributes.html) stores per-partition display properties.
- [vtkCompositePolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkCompositePolyDataMapper.html) renders all partitions. `SetBlockColor()` assigns distinct colors using flat indices.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a cube.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates a cylinder.
- [vtkPartitionedDataSet](https://www.vtk.org/doc/nightly/html/classvtkPartitionedDataSet.html) groups datasets as flat partitions without hierarchical nesting. Unlike vtkMultiBlockDataSet, all partitions are at the same level. `SetPartition()` assigns each dataset by index.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html), [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html), [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html), and [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generate four geometric objects positioned side by side.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
