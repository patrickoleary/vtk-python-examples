### Description

This example demonstrates motion blur using vtkSimpleMotionBlurPass on the Armadillo mesh rendered with three different material properties.

**Reader → Mapper → Actor → RenderPass → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with distinct material properties.
- [vtkPLYReader](https://www.vtk.org/doc/nightly/html/classvtkPLYReader.html) loads the Armadillo mesh from a `.ply` file.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the mesh to graphics primitives.
- [vtkRenderStepsPass](https://www.vtk.org/doc/nightly/html/classvtkRenderStepsPass.html) provides the default rendering steps that the motion blur pass wraps.
- [vtkSimpleMotionBlurPass](https://www.vtk.org/doc/nightly/html/classvtkSimpleMotionBlurPass.html) accumulates sub-frames to produce the motion blur effect.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
