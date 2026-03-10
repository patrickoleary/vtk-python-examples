### Description

This example volumes render a transient unstructured grid using vtkTimeSourceExample. The time source produces an unstructured grid with time-varying point scalars ("Point Label"). The grid is tetrahedralized with vtkDataSetTriangleFilter (required by the unstructured grid volume mapper), then rendered with blue-to-red coloring.

**TimeSourceExample → DataSetTriangleFilter → UnstructuredGridVolumeRayCastMapper → Volume + ScalarBar + TextActor → Renderer → RenderWindow → Interactor (timer animation)**

- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) maps scalar values to RGB colors.
- [vtkDataSetTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkDataSetTriangleFilter.html) tetrahedralizes the grid for volume rendering.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkOpenGLRayCastImageDisplayHelper](https://www.vtk.org/doc/nightly/html/classvtkOpenGLRayCastImageDisplayHelper.html) provides open glray cast image display helper functionality.
- [vtkPiecewiseFunction](https://www.vtk.org/doc/nightly/html/classvtkPiecewiseFunction.html) maps scalar values to opacity.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the color legend.
- [vtkStreamingDemandDrivenPipeline](https://www.vtk.org/doc/nightly/html/classvtkStreamingDemandDrivenPipeline.html) provides streaming demand driven pipeline functionality.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) displays the current time step.
- [vtkTimeSourceExample](https://www.vtk.org/doc/nightly/html/classvtkTimeSourceExample.html) produces a time-varying unstructured grid with configurable time steps.
- [vtkUnstructuredGridVolumeRayCastMapper](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGridVolumeRayCastMapper.html) performs ray-cast volume rendering on unstructured grids.
- [vtkVolume](https://www.vtk.org/doc/nightly/html/classvtkVolume.html) pairs the volume mapper with its properties.
- [vtkVolumeProperty](https://www.vtk.org/doc/nightly/html/classvtkVolumeProperty.html) combines color and opacity transfer functions.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
