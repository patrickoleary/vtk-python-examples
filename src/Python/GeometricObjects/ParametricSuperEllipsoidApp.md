### Description

This example interactives demo of a super-ellipsoid parametric surface. Two sliders control the N1 (Z squareness) and N2 (XY squareness) exponents in real time. It follows the VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor → Widget**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) renders the front face in banana yellow and the back face in tomato red via a separate [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html).
- [vtkCommand](https://www.vtk.org/doc/nightly/html/classvtkCommand.html) provides command functionality.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) samples the parametric function to produce polygonal output.
- [vtkParametricSuperEllipsoid](https://www.vtk.org/doc/nightly/html/classvtkParametricSuperEllipsoid.html) defines the super-ellipsoid equations with adjustable N1 and N2 exponents.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface geometry to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkSliderRepresentation2D](https://www.vtk.org/doc/nightly/html/classvtkSliderRepresentation2D.html) 2D slider representation.
- [vtkSliderWidget](https://www.vtk.org/doc/nightly/html/classvtkSliderWidget.html) provides two interactive sliders that update the surface exponents via lambda callbacks.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a dark blue background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
