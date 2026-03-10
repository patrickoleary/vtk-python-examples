### Description

This example generates 2D contour lines on a CT head slice using vtkFlyingEdges2D.

**Reader → ExtractVOI → FlyingEdges2D → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkExtractVOI](https://www.vtk.org/doc/nightly/html/classvtkExtractVOI.html) extracts a single axial slice.
- [vtkFlyingEdges2D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges2D.html) generates 2D contour lines on the slice.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the CT head volume.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates the bounding outline.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
