### Description

This example clips a 51³ rectilinear grid with a cone polydata using vtkImplicitPolyDataDistance and vtkClipDataSet. Two separate clippers extract the inside (left) and outside (right) portions. A tomato-red cone wireframe and a black bounding-box outline appear in both viewports so the relationship between the clip surface and the results is clear. It follows the VTK pipeline structure:

**ConeSource → ImplicitPolyDataDistance → RectilinearGrid + ClipDataSet (×2) → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — inside and outside clips shown in banana yellow, with tomato-red cone wireframes and black outlines in each viewport.
- [vtkClipDataSet](https://www.vtk.org/doc/nightly/html/classvtkClipDataSet.html) — two separate clippers using `SetClipFunction()`: one with `InsideOutOn()` for the inside portion and one with `InsideOutOff()` for the outside portion.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone pointing downward with 50-sided resolution and capping enabled. A tomato-red wireframe of the cone is shown in both viewports as the clip surface reference.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the clipped volumes to graphics primitives.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkImplicitPolyDataDistance](https://www.vtk.org/doc/nightly/html/classvtkImplicitPolyDataDistance.html) converts the cone surface into an implicit signed-distance function used as the clip function.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates a black bounding-box wireframe around the rectilinear grid.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRectilinearGrid](https://www.vtk.org/doc/nightly/html/classvtkRectilinearGrid.html) defines a 51×51×51 uniform grid over [−1, 1]³.
- [vtkRectilinearGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkRectilinearGridGeometryFilter.html) translucent outer skin of the rectilinear grid with edges.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers in side-by-side viewports sharing one camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
