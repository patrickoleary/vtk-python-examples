### Description

This example clips a coarse 15³ rectilinear grid with a cone polydata using vtkImplicitPolyDataDistance and vtkClipDataSet. Four color-coded wireframe layers show the cone clip surface (tomato red), the clipped grid cells inside the cone (steel blue), a mid-Z slice of the original grid (light gray), and a black bounding-box outline around the grid. It follows the VTK pipeline structure:

**ConeSource → ImplicitPolyDataDistance → RectilinearGrid + ClipDataSet → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — four wireframe actors: the cone clip surface (tomato red), the clipped grid cells (steel blue), the background grid slice (light gray), and the bounding-box outline (black).
- [vtkClipDataSet](https://www.vtk.org/doc/nightly/html/classvtkClipDataSet.html) clips the grid at the zero isovalue. `InsideOutOn()` retains the region inside the cone.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates a cone with 20-sided resolution. A tomato-red wireframe of the cone is displayed as the clip surface reference.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the clipped mesh as a steel-blue wireframe.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkImplicitPolyDataDistance](https://www.vtk.org/doc/nightly/html/classvtkImplicitPolyDataDistance.html) converts the cone surface into an implicit signed-distance function.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates a black bounding-box wireframe around the rectilinear grid.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRectilinearGrid](https://www.vtk.org/doc/nightly/html/classvtkRectilinearGrid.html) defines a 15×15×15 coarse grid over [−1, 1]³ with signed-distance scalars.
- [vtkRectilinearGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkRectilinearGridGeometryFilter.html) extracts a mid-Z slice of the grid for light-gray wireframe context.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
