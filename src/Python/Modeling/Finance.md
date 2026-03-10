### Description

This example visualizes multidimensional financial data using vtkGaussianSplatter and vtkContourFilter. The gray translucent surface represents the total loan population and the red surface highlights delinquent payments. Tube axes provide spatial reference. It follows the VTK pipeline structure:

**financial.txt → UnstructuredGrid → GaussianSplatter → ContourFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — three actors: total population (gray, 30% opacity), delinquent population (red), and tube axes.
- [vtkAxes](https://www.vtk.org/doc/nightly/html/classvtkAxes.html) and [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) create colored tube axes at the data origin.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts isosurfaces from each splattered volume at value 0.01.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkGaussianSplatter](https://www.vtk.org/doc/nightly/html/classvtkGaussianSplatter.html) — two splatters: one for the total population (scalar warping off) and one for the delinquent subset (scalar warping on).
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surfaces and axes to graphics primitives.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) generates tubes around lines.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) holds the financial data points with monthly payment, interest rate, and loan amount as coordinates and time-late as a scalar.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
