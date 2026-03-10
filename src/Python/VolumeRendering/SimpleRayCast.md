### Description

This example volumes rendering of a high potential iron protein using a fixed-point volume ray cast mapper. Transfer functions map scalar values to color and opacity.

**Reader → VolumeMapper → VolumeProperty → Volume → Renderer → RenderWindow → Interactor**

- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines the scalar-to-color transfer function.
- [vtkFixedPointVolumeRayCastMapper](https://www.vtk.org/doc/nightly/html/classvtkFixedPointVolumeRayCastMapper.html) performs the volume ray casting.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors for the background.
- [vtkOpenGLRayCastImageDisplayHelper](https://www.vtk.org/doc/nightly/html/classvtkOpenGLRayCastImageDisplayHelper.html) provides open glray cast image display helper functionality.
- [vtkPiecewiseFunction](https://www.vtk.org/doc/nightly/html/classvtkPiecewiseFunction.html) defines the scalar-to-opacity transfer function.
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) reads the iron protein structured points dataset.
- [vtkVolume](https://www.vtk.org/doc/nightly/html/classvtkVolume.html) holds the mapper and property and represents the volume in the scene.
- [vtkVolumeProperty](https://www.vtk.org/doc/nightly/html/classvtkVolumeProperty.html) describes shading, interpolation, and transfer functions for the volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
