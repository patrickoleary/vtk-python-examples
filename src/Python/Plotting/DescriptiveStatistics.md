### Description

This example demonstrates vtkDescriptiveStatistics to compute mean, standard deviation, min, max, and count of Gaussian-distributed random data, then displays the data as a scatter plot with a text overlay showing the computed statistics.

**Table → DescriptiveStatistics → TextMapper → Actor2D + Glyph3DMapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkActor2D](https://www.vtk.org/doc/nightly/html/classvtkActor2D.html) positions the text overlay on screen.
- [vtkDescriptiveStatistics](https://www.vtk.org/doc/nightly/html/classvtkDescriptiveStatistics.html) computes descriptive statistics (mean, standard deviation, min, max, etc.) on table columns.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkGlyph3DMapper](https://www.vtk.org/doc/nightly/html/classvtkGlyph3DMapper.html) places sphere glyphs at each data point.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the glyph shape.
- [vtkTable](https://www.vtk.org/doc/nightly/html/classvtkTable.html) holds the input data.
- [vtkTextMapper](https://www.vtk.org/doc/nightly/html/classvtkTextMapper.html) renders the statistics as a text overlay.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
