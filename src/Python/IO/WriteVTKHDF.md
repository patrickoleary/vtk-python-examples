### Description

This example writes a VTK dataset to the VTKHDF file format using vtkHDFWriter, then reads it back with vtkHDFReader and renders the result. The round-trip demonstrates the modern HDF5-based VTK file format with scalar data preserved. It follows the VTK pipeline structure:

**Source → ElevationFilter → Writer → Reader → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) computes an elevation scalar field along the Y axis. `SetLowPoint()` and `SetHighPoint()` define the scalar range direction.
- [vtkHDFReader](https://www.vtk.org/doc/nightly/html/classvtkHDFReader.html) reads the VTKHDF file back, producing the same dataset that was written.
- [vtkHDFWriter](https://www.vtk.org/doc/nightly/html/classvtkHDFWriter.html) writes the polydata to a `.vtkhdf` file. `SetOverwrite(True)` replaces an existing file. The VTKHDF format is HDF5-based, supports compression, and can store `vtkPolyData`, `vtkUnstructuredGrid`, `vtkPartitionedDataSet`, `vtkMultiBlockDataSet`, and `vtkPartitionedDataSetCollection`.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the round-tripped polydata to graphics primitives. `SetScalarRange()` maps the elevation scalars to the default color lookup table.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere polygon mesh with `SetThetaResolution(32)` and `SetPhiResolution(32)`.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
