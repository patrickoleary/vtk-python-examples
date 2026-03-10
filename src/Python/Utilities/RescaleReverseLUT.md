### Description

This example rescales and reverses a color transfer function, displayed in a 2×2 viewport grid. Newton's original seven rainbow colors are used as the base colormap. The four variants shown are: original, rescaled to [0,1], reversed, and both rescaled and reversed.

**CylinderSource → ElevationFilter → Mapper (×4 CTF variants) + ScalarBarActor + TextActor → Renderer (×4) → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) displays the 2D title text.
- [vtkCylinderSource](https://www.vtk.org/doc/nightly/html/classvtkCylinderSource.html) generates the cylinder geometry.
- [vtkDiscretizableColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkDiscretizableColorTransferFunction.html) defines and manipulates the color transfer function.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) maps vertical position to scalar values.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps elevation scalars through the CTF.
- [vtkScalarBarActor](https://www.vtk.org/doc/nightly/html/classvtkScalarBarActor.html) displays the color bar legend.
- [vtkTextMapper](https://www.vtk.org/doc/nightly/html/classvtkTextMapper.html) renders the viewport title text.
- [vtkTextProperty](https://www.vtk.org/doc/nightly/html/classvtkTextProperty.html) configures text font and color.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles each viewport.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
