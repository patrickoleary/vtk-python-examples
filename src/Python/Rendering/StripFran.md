### Description

This example compares triangle-strip versus unstructured mesh rendering on the Fran face dataset, showing every other polygon in a side-by-side view.

**Reader → DecimatePro → Stripper → MaskPolyData → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) provides a shared camera across the two viewports.
- [vtkDecimatePro](https://www.vtk.org/doc/nightly/html/classvtkDecimatePro.html) reduces the polygon count of the face mesh.
- [vtkMaskPolyData](https://www.vtk.org/doc/nightly/html/classvtkMaskPolyData.html) selects every Nth polygon for display.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polygon data to graphics primitives.
- [vtkPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkPolyDataReader.html) loads the Fran face dataset from a legacy `.vtk` file.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) converts the polygons into triangle strips.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
