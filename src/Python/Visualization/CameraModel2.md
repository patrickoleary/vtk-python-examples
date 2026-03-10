### Description

This example illustrates camera movement centered at the camera position (yaw, pitch, roll).

**Sources → ImplicitModel → Contour → Warp → Transform → Mapper → Actors → Text → Renderer → Window → Interactor**

- [vtkAppendPolyData](https://www.vtk.org/doc/nightly/html/classvtkAppendPolyData.html) combines the camera lens and body.
- [vtkCellArray](https://www.vtk.org/doc/nightly/html/classvtkCellArray.html) stores cell connectivity.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates the camera lens geometry.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts an isosurface from the distance field.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates the camera body geometry.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps dataset to graphics primitives.
- [vtkImplicitModeller](https://www.vtk.org/doc/nightly/html/classvtkImplicitModeller.html) creates a distance field from the arrow shape.
- [vtkLODActor](https://www.vtk.org/doc/nightly/html/classvtkLODActor.html) assigns geometry with level-of-detail rendering.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) represents polygonal geometry.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkRotationalExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkRotationalExtrusionFilter.html) generates the direction-of-projection spike.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the focal point sphere.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) displays text labels for yaw, pitch, and roll.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) rotates and scales the arrow geometry.
- [vtkTransformFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformFilter.html) applies the transform to the arrow.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) transforms polydata for the spike profile.
- [vtkWarpTo](https://www.vtk.org/doc/nightly/html/classvtkWarpTo.html) warps the isosurface into a curved arrow.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
