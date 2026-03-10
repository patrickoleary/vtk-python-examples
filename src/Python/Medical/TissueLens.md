### Description

This example creates a "tissue lens" effect on a CT head dataset. The skin isosurface is clipped by a sphere, and a probe filter samples the volume inside the sphere to reveal internal tissue intensities on the spherical surface. A grayscale lookup table maps the probed scalar values.

**Reader → FlyingEdges3D → ClipDataSet (Sphere) + SphereSource → ProbeFilter → ClipDataSet → DataSetMapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene.
- [vtkCamera](https://www.vtk.org/doc/nightly/html/classvtkCamera.html) defines the viewpoint and projection.
- [vtkClipDataSet](https://www.vtk.org/doc/nightly/html/classvtkClipDataSet.html) clips the skin surface and the probed sphere.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps unstructured clip output to graphics primitives.
- [vtkFlyingEdges3D](https://www.vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) extracts the skin isosurface at contour value 500.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) defines a grayscale mapping for tissue intensities.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the MetaImage (.mhd/.raw) CT volume.
- [vtkProbeFilter](https://www.vtk.org/doc/nightly/html/classvtkProbeFilter.html) samples the volume onto the sphere surface.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines surface appearance (color, lighting, representation).
- [vtkSphere](https://www.vtk.org/doc/nightly/html/classvtkSphere.html) defines the implicit spherical clip function.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the lens sphere geometry.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
