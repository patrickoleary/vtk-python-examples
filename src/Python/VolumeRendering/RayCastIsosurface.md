### Description

This example uses GPU volume ray casting in iso-surface blend mode to produce an iso-surface-like image of a CT head dataset. Two iso-surface values are rendered with different colors and opacities.

**MetaImageReader → GPUVolumeRayCastMapper → VolumeProperty → Volume → Renderer → RenderWindow → Interactor**

- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) positions the viewpoint for a good view of the head.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines the scalar-to-color transfer function.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) provides trackball-style camera interaction.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the FullHead meta image dataset.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkOpenGLGPUVolumeRayCastMapper](https://www.vtk.org/doc/nightly/html/classvtkOpenGLGPUVolumeRayCastMapper.html) performs GPU-accelerated volume ray casting with iso-surface blend mode.
- [vtkPiecewiseFunction](https://www.vtk.org/doc/nightly/html/classvtkPiecewiseFunction.html) defines the scalar-to-opacity transfer function.
- [vtkVolume](https://www.vtk.org/doc/nightly/html/classvtkVolume.html) holds the mapper and property and represents the volume in the scene.
- [vtkVolumeProperty](https://www.vtk.org/doc/nightly/html/classvtkVolumeProperty.html) describes shading, interpolation, transfer functions, and iso-surface values.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
