### Description

This example visualizes marching cubes case 7 for 3D isosurface generation.

**UnstructuredGrid → ContourFilter → ExtractEdges → TubeFilter → Mapper → Actor | ShrinkPolyData → Mapper → Actor | ThresholdPoints → Glyph3D → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) finds the isosurface triangles.
- [vtkCubeSource](https://www.vtk.org/doc/nightly/html/classvtkCubeSource.html) generates a cube.
- [vtkExtractEdges](https://www.vtk.org/doc/nightly/html/classvtkExtractEdges.html) extracts triangle and cube edges.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) stores float data arrays.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places sphere glyphs at active vertices.
- [vtkIdList](https://www.vtk.org/doc/nightly/html/classvtkIdList.html) stores lists of VTK ids.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkShrinkPolyData](https://www.vtk.org/doc/nightly/html/classvtkShrinkPolyData.html) shrinks contour triangles for clarity.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere.
- [vtkThresholdPoints](https://www.vtk.org/doc/nightly/html/classvtkThresholdPoints.html) selects active vertices.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) positions the label.
- [vtkTubeFilter](https://www.vtk.org/doc/nightly/html/classvtkTubeFilter.html) renders edges as tubes.
- [vtkUnstructuredGrid](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGrid.html) defines the hexahedron cell with scalar values.
- [vtkVectorText](https://www.vtk.org/doc/nightly/html/classvtkVectorText.html) generates the case label text.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
