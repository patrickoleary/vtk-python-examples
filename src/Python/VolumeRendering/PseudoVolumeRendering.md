### Description

This example pseudos volume rendering using 20 translucent cut planes composited back-to-front to simulate volume rendering of a PLOT3D combustor dataset. An isosurface and outline provide additional context.

**PLOT3DReader → ExtractGrid → Cutter → Mapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an isosurface for context.
- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) generates cut planes sorted by cell for back-to-front compositing.
- [vtkExtractGrid](https://www.vtk.org/doc/nightly/html/classvtkExtractGrid.html) limits the volume of interest for experimentation.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps scalar values to colors with translucent alpha.
- [vtkMultiBlockPLOT3DReader](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockPLOT3DReader.html) reads the PLOT3D structured grid data (geometry and solution).
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit cutting plane.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes normals for smooth isosurface shading.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) creates triangle strips from the outline for tube generation.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates a bounding box outline.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) renders the outline as tubes.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
