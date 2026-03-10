### Description

This example demonstrates vtkPartitionedDataSetCollection by grouping three partitioned datasets (spheres, cubes, and a cone) into a collection and rendering with per-block coloring. Each partitioned dataset contains one or more partitions of the same object type.

**Sources → Partitioned Datasets → Collection → Composite Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the composite mapper to the scene. Per-block colors are set on the mapper rather than the actor.
- [vtkCompositeDataDisplayAttributes](https://www.vtk.org/doc/nightly/html/classvtkCompositeDataDisplayAttributes.html) stores per-block display properties.
- [vtkCompositePolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkCompositePolyDataMapper.html) renders all blocks. Flat indices walk the tree depth-first: root → each partitioned dataset → each partition within.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a cube.
- [vtkPartitionedDataSet](https://www.vtk.org/doc/nightly/html/classvtkPartitionedDataSet.html) groups datasets as flat partitions. Three separate partitioned datasets hold spheres, cubes, and a cone respectively.
- [vtkPartitionedDataSetCollection](https://www.vtk.org/doc/nightly/html/classvtkPartitionedDataSetCollection.html) organizes multiple partitioned datasets into a single collection. This is the modern replacement for deeply nested vtkMultiBlockDataSet hierarchies. `SetPartitionedDataSet()` assigns each group by index.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html), [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html), and [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generate geometric objects at different positions.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
