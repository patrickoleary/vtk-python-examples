### Description

This example builds a color transfer function from an inline Spectral JSON colormap. The Spectral colormap, based on the ColorBrewer scheme, is a diverging palette that transitions from red through orange and yellow to green and blue. It is effective for data that diverges around a central value.

**ParametricSuperEllipsoid → ElevationFilter → Mapper (with Spectral CTF) → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDiscretizableColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkDiscretizableColorTransferFunction.html) defines the Spectral color transfer function from parsed JSON.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) maps vertical position to scalar values.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) tessellates the parametric function into polygon data.
- [vtkParametricSuperEllipsoid](https://www.vtk.org/doc/nightly/html/classvtkParametricSuperEllipsoid.html) defines the super-ellipsoid parametric function.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps elevation scalars through the CTF.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
