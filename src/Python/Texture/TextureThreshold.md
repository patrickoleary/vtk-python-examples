### Description

This example demonstrates texture thresholding applied to scalar data from a simulation of fluid flow around a blunt fin. Three cutting planes slice through the dataset at different positions, each with a different scalar threshold applied via vtkThresholdTextureCoords.

**PLOT3DReader → StructuredGridGeometryFilter → ThresholdTextureCoords + Texture → DataSetMapper → Actor → Renderer → RenderWindow → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry and texture.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) positions the viewpoint.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the thresholded planes to graphics primitives.
- [vtkMultiBlockPLOT3DReader](https://www.vtk.org/doc/nightly/html/classvtkMultiBlockPLOT3DReader.html) reads the blunt fin PLOT3D dataset (geometry + solution).
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the wall and fin geometry.
- [vtkStructuredGridGeometryFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridGeometryFilter.html) extracts 2D surface slices from the 3D structured grid.
- [vtkStructuredGridOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkStructuredGridOutlineFilter.html) generates a wireframe outline for context.
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) reads the boolean texture map.
- [vtkTexture](https://www.vtk.org/doc/nightly/html/classvtkTexture.html) applies the threshold texture to each plane actor.
- [vtkThresholdTextureCoords](https://www.vtk.org/doc/nightly/html/classvtkThresholdTextureCoords.html) generates texture coordinates based on scalar thresholds.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
