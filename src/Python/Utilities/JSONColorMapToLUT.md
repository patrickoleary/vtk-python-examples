### Description

This example builds a vtkDiscretizableColorTransferFunction from an inline JSON colormap definition. The JSON format matches the ParaView colormap export format, making it easy to transfer colormaps between ParaView and VTK Python code.

**SphereSource → ElevationFilter → Mapper (with JSON-derived CTF) → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDiscretizableColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkDiscretizableColorTransferFunction.html) defines a color transfer function from the parsed JSON data.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) maps vertical position to scalar values.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps elevation scalars through the color transfer function.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
