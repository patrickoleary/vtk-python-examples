### Description

This example aligns two polydata meshes (cow.vtp and cowHead.vtp) using OBB-based landmark alignment followed by Iterative Closest Point refinement. The Hausdorff distance is computed before and after alignment to measure the fit.

**Reader → OBBTree → LandmarkTransform → IterativeClosestPointTransform → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCameraOrientationWidget](https://www.vtk.org/doc/nightly/html/classvtkCameraOrientationWidget.html) provides an interactive orientation gizmo.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the aligned meshes to graphics primitives.
- [vtkHausdorffDistancePointSetFilter](https://www.vtk.org/doc/nightly/html/classvtkHausdorffDistancePointSetFilter.html) computes the distance metric between the two meshes.
- [vtkIterativeClosestPointTransform](https://www.vtk.org/doc/nightly/html/classvtkIterativeClosestPointTransform.html) refines the alignment with a rigid-body ICP step.
- [vtkLandmarkTransform](https://www.vtk.org/doc/nightly/html/classvtkLandmarkTransform.html) aligns the OBB corners of the source to the target.
- [vtkOBBTree](https://www.vtk.org/doc/nightly/html/classvtkOBBTree.html) computes oriented bounding boxes for initial alignment.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores landmark point sets for the bounding-box alignment.
- [vtkPolyData](https://www.vtk.org/doc/nightly/html/classvtkPolyData.html) holds the source and target mesh geometry.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) composes rotation transforms when testing OBB orientations.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies the best transform to the source mesh.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) loads the source and target meshes from `.vtp` files.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
