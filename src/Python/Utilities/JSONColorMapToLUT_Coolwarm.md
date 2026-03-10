### Description

This example builds a color transfer function from an inline Cool to Warm JSON colormap. This diverging colormap, designed by Kenneth Moreland, transitions from blue through white to red. It is ideal for visualizing data with a meaningful midpoint, such as temperature deviations or signed distances.

**ParametricTorus → ElevationFilter → Mapper (with Coolwarm CTF) → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDiscretizableColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkDiscretizableColorTransferFunction.html) defines the Cool to Warm color transfer function from parsed JSON.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) maps vertical position to scalar values.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the parametric torus into polygon data.
- [vtkParametricTorus](https://www.vtk.org/doc/nightly/html/classvtkParametricTorus.html) defines the torus parametric function.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps elevation scalars through the CTF.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
