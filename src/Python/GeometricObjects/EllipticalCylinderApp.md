### Description

This example extrudes an elliptical cross-section into a semi-transparent cylinder, showing the base polyline as a tube and the extrusion vector as an oriented arrow. It follows the VTK pipeline structure:

**Data → Filter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns colors and opacity — banana for the cylinder surface (70% opacity), peacock for the tube, tomato for the arrow.
- [vtkArrowSource](https://www.vtk.org/doc/nightly/html/classvtkArrowSource.html) generates an arrow glyph oriented along the extrusion vector using [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) and a direction cosine matrix built from [vtkMatrix4x4](https://www.vtk.org/doc/nightly/html/classvtkMatrix4x4.html).
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) positions the view with `Azimuth()` and `Elevation()`.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkInteractorStyleTrackballCamera](https://www.vtk.org/doc/nightly/html/classvtkInteractorStyleTrackballCamera.html) maps mouse motion to camera transformations.
- [vtkLinearExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkLinearExtrusionFilter.html) extrudes the cross-section along a vector via `SetVector()`.
- [vtkMath](https://www.vtk.org/doc/nightly/html/classvtkMath.html) provides mathematical utility functions.
- [vtkMatrix4x4](https://www.vtk.org/doc/nightly/html/classvtkMatrix4x4.html) provides matrix4x4 functionality.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) provides minimal standard random sequence functionality.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) and [vtkPolyLine](https://www.vtk.org/doc/nightly/html/classvtkPolyLine.html) define the elliptical cross-section stored in a [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html).
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each element to graphics primitives.
- [vtkPolyLine](https://www.vtk.org/doc/nightly/html/classvtkPolyLine.html) connect the ellipse points into a closed loop.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies a geometric transformation to polydata.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) thickens the base polyline into a visible tube.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a slate gray background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
