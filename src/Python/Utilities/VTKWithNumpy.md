### Description

This example volumes render a numpy array containing three overlapping colored cubes. This demonstrates how to transfer numpy data into VTK using vtkImageImport and render it with the volume rendering pipeline.

**numpy → vtkImageImport → VolumeMapper → Volume (with color + opacity TFs) → Renderer → RenderWindow → Interactor**

- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) maps scalar values to RGB colors.
- [vtkFixedPointVolumeRayCastMapper](https://www.vtk.org/doc/nightly/html/classvtkFixedPointVolumeRayCastMapper.html) performs ray-cast volume rendering.
- [vtkImageImport](https://www.vtk.org/doc/nightly/html/classvtkImageImport.html) transfers a raw byte buffer (from numpy) into VTK as image data.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkOpenGLRayCastImageDisplayHelper](https://www.vtk.org/doc/nightly/html/classvtkOpenGLRayCastImageDisplayHelper.html) provides open glray cast image display helper functionality.
- [vtkPiecewiseFunction](https://www.vtk.org/doc/nightly/html/classvtkPiecewiseFunction.html) maps scalar values to opacity.
- [vtkVolume](https://www.vtk.org/doc/nightly/html/classvtkVolume.html) pairs the volume mapper with its properties.
- [vtkVolumeProperty](https://www.vtk.org/doc/nightly/html/classvtkVolumeProperty.html) combines the color and opacity transfer functions.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
