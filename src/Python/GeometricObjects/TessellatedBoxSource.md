### Description

This example renders a tessellated box with shrunk faces and visible edges using vtkTessellatedBoxSource and vtkShrinkFilter. It follows the VTK pipeline structure:

**Source → Filter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns visual properties to the mapped geometry.
- [vtkAlgorithm](https://www.vtk.org/doc/nightly/html/classvtkAlgorithm.html) provides algorithm functionality.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the shrunk dataset to graphics primitives.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines the backface color (tomato). The front face is banana with `EdgeVisibilityOn()`.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) shrinks each cell toward its centroid, visually separating adjacent faces.
- [vtkTessellatedBoxSource](https://www.vtk.org/doc/nightly/html/classvtkTessellatedBoxSource.html) generates a box whose faces are subdivided into quads or triangles. `SetLevel()` controls the subdivision depth and `SetBounds()` defines the box extents.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a silver background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
