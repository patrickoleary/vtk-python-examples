### Description

This example creates contours from a CT head slice image using vtkMarchingSquares and triangulates the enclosed region with vtkContourTriangulator. The orchid contour lines overlay the gray triangulated fill. It follows the VTK pipeline structure:

**PNGReader → MarchingSquares → ContourTriangulator → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) — two actors: the contour lines (medium orchid) and the triangulated fill (gray).
- [vtkContourTriangulator](https://www.vtk.org/doc/nightly/html/classvtkContourTriangulator.html) fills the contour region with triangles.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the contour lines and triangulated region to graphics primitives.
- [vtkMarchingSquares](https://www.vtk.org/doc/nightly/html/classvtkMarchingSquares.html) extracts contour lines at iso value 500.
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) loads a CT head slice image (fullhead15.png).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
