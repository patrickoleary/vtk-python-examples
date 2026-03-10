### Description

This example visualizes an implicit cylinder by sampling it on a volume grid using vtkSampleFunction and extracting the zero isosurface with vtkContourFilter. The cylinder is infinite along the Y axis with radius 0.5, clipped by the sampling bounds to produce a finite tube rendered in tomato red. It follows the VTK pipeline structure:

**Cylinder → SampleFunction → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene with tomato red color.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts the zero isosurface — the cylindrical surface clipped by the sampling bounds.
- [vtkCylinder](https://www.vtk.org/doc/nightly/html/classvtkCylinder.html) defines an implicit cylinder function. The cylinder axis is along Y by default. `SetRadius(0.5)` sets the cross-section radius. The implicit function evaluates to `x² + z² - r²` at any point.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the contour surface to graphics primitives.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) evaluates the implicit cylinder on a regular 50×50×50 grid over [−1, 1]³, producing a scalar volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `GetActiveCamera().Azimuth()` and `Elevation()` tilt the view.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
