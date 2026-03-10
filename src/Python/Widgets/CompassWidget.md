### Description

This example uses a compass widget to control camera heading, tilt, and distance around an annotated cube.

**AnnotatedCubeActor → CompassWidget → Renderer → Window → Interactor**

- [vtkAnnotatedCubeActor](https://www.vtk.org/doc/nightly/html/classvtkAnnotatedCubeActor.html) provides a labelled cube to orient the camera around.
- [vtkCommand](https://www.vtk.org/doc/nightly/html/classvtkCommand.html) provides command functionality.
- [vtkCompassRepresentation](https://www.vtk.org/doc/nightly/html/classvtkCompassRepresentation.html) renders the compass dial, sliders, and distance ring.
- [vtkCompassWidget](https://www.vtk.org/doc/nightly/html/classvtkCompassWidget.html) provides heading, tilt, and distance controls for the camera.
- [vtkMath](https://www.vtk.org/doc/nightly/html/classvtkMath.html) provides mathematical utility functions.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named color lookup.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
