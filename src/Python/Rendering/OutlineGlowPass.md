### Description

This example highlights an arrow with a glowing outline using vtkOutlineGlowPass on a layered renderer on top of the main scene.

**Source → Mapper → Actor → RenderPass → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkArrowSource](https://www.vtk.org/doc/nightly/html/classvtkArrowSource.html) generates the arrow polygon data.
- [vtkOutlineGlowPass](https://www.vtk.org/doc/nightly/html/classvtkOutlineGlowPass.html) applies a glowing outline effect around actors rendered by the delegate pass.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the arrow polygon data to graphics primitives.
- [vtkRenderStepsPass](https://www.vtk.org/doc/nightly/html/classvtkRenderStepsPass.html) provides the default rendering steps that the outline glow pass wraps.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. Two renderers on separate layers provide the glow overlay.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
