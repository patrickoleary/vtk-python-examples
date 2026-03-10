### Description

This example volumes rendering of a procedural multi-block dataset consisting of 8 colored blocks arranged in a 2x2x2 grid. Each block is a small vtkImageData volume filled with a distinct color from a Brewer qualitative color scheme.

**Procedural MultiBlockDataSet → MultiBlockVolumeMapper → VolumeProperty → Volume → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the outline geometry.
- [vtkColorSeries](https://www.vtk.org/doc/nightly/html/classvtkColorSeries.html) provides a qualitative color scheme for the blocks.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) represents each individual volume block.
- [vtkMultiBlockDataSet](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockDataSet.html) holds the 8 procedural image data blocks.
- [vtkMultiBlockVolumeMapper](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockVolumeMapper.html) renders multi-block volume data on the GPU.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors for the background and outline.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates a bounding box outline around the dataset.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the outline polygon data to graphics primitives.
- [vtkVolume](https://www.vtk.org/doc/nightly/html/classvtkVolume.html) holds the mapper and property and represents the volume in the scene.
- [vtkVolumeProperty](https://www.vtk.org/doc/nightly/html/classvtkVolumeProperty.html) describes volume rendering properties with non-independent RGBA components.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
