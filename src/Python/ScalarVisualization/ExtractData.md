### Description

This example extracts geometry from a sampled quadric using a boolean union of spheres.

**Quadric → SampleFunction → ExtractGeometry → ShrinkFilter → Mapper → Actor | OutlineFilter → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the dataset to graphics primitives.
- [vtkExtractGeometry](https://www.vtk.org/doc/nightly/html/classvtkExtractGeometry.html) extracts geometry within the boolean region.
- [vtkImplicitBoolean](https://www.vtk.org/doc/nightly/html/classvtkImplicitBoolean.html) combines the spheres with a boolean union.
- [vtkOutlineFilter](https://www.vtk.org/doc/nightly/html/classvtkOutlineFilter.html) generates the bounding outline.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkQuadric](https://www.vtk.org/doc/nightly/html/classvtkQuadric.html) defines the quadric implicit function.
- [vtkSampleFunction](https://www.vtk.org/doc/nightly/html/classvtkSampleFunction.html) samples the implicit function on a regular grid.
- [vtkShrinkFilter](https://www.vtk.org/doc/nightly/html/classvtkShrinkFilter.html) shrinks the extracted cells for visual clarity.
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) defines the sphere implicit functions.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) applies anisotropic scaling to the spheres.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
