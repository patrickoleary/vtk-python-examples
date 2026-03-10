### Description

This example glyphs cone spikes along surface normals of a laser-digitized face mesh.

**Reader → PolyDataNormals → MaskPoints → Glyph3D → Mapper → Actor | Reader → PolyDataNormals → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkConeSource](https://www.vtk.org/doc/nightly/html/classvtkConeSource.html) generates the cone glyph shape.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places oriented cone glyphs at subsampled surface points.
- [vtkMaskPoints](https://www.vtk.org/doc/nightly/html/classvtkMaskPoints.html) subsamples every 10th point for glyphing.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataNormals](https://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html) computes and flips surface normals to point outward.
- [vtkPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkPolyDataReader.html) loads the Cyberware laser-digitized face mesh.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines a 4×4 geometric transformation.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) translates the cone so its base is at the origin.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
