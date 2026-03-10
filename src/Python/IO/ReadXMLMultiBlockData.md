### Description

This example reads a VTK XML multi-block dataset (.vtm) file using vtkXMLMultiBlockDataReader and display the blocks. A small multi-block dataset (sphere + cube) is generated and written to disk if the file does not already exist.

**Reader → CompositePolyDataMapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCompositePolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkCompositePolyDataMapper.html) renders multi-block polydata directly.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a cube.
- [vtkMultiBlockDataSet](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockDataSet.html) provides multi block data set functionality.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkXMLMultiBlockDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLMultiBlockDataReader.html) reads VTK XML multi-block dataset files.
- [vtkXMLMultiBlockDataWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLMultiBlockDataWriter.html) writes VTK XML multi-block files (used to generate sample data).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
