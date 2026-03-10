### Description

This example scales a sphere non-uniformly with vtkTransformFilter and colour it by elevation through a blue-to-red lookup table.

**Source → TransformFilter → ElevationFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the elevation-coloured data to graphics primitives.
- [vtkElevationFilter](https://www.vtk.org/doc/nightly/html/classvtkElevationFilter.html) computes scalar values based on height.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps elevation scalars to a blue-to-red colour ramp.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the input sphere polydata.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) defines the non-uniform scaling.
- [vtkTransformFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformFilter.html) applies the non-uniform scale to the sphere.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
