### Description

This example minimums intensity projection volume rendering of an iron protein. The volume is clipped to a thin slab to reveal the minimum intensity structures within.

**Reader → ImageClip → VolumeMapper (MinIntensity) → VolumeProperty → Volume → Renderer → RenderWindow → Interactor**

- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines the scalar-to-color transfer function.
- [vtkFixedPointVolumeRayCastMapper](https://www.vtk.org/doc/nightly/html/classvtkFixedPointVolumeRayCastMapper.html) performs volume ray casting with minimum intensity blend mode.
- [vtkImageClip](https://www.vtk.org/doc/nightly/html/classvtkImageClip.html) crops the volume to a thin slab for minimum intensity visibility.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors for the background.
- [vtkPiecewiseFunction](https://www.vtk.org/doc/nightly/html/classvtkPiecewiseFunction.html) defines the scalar-to-opacity transfer function.
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) reads the iron protein structured points dataset.
- [vtkVolume](https://www.vtk.org/doc/nightly/html/classvtkVolume.html) holds the mapper and property and represents the volume in the scene.
- [vtkVolumeProperty](https://www.vtk.org/doc/nightly/html/classvtkVolumeProperty.html) describes interpolation and transfer functions for the volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
