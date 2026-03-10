### Description

This example displays all five Platonic solids arranged in a row within a single scene. Each face is colored using a lookup table so adjacent faces are visually distinct. It follows the VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) positions each solid along the x-axis with `SetPosition()`.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps the 20 possible cell scalars to distinct colors.
- [vtkPlatonicSolidSource](https://www.vtk.org/doc/nightly/html/classvtkPlatonicSolidSource.html) generates each solid by type index (0–4). Each face receives a unique cell scalar.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each solid's geometry and scalars to graphics primitives.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays text in the viewport.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a slate gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
