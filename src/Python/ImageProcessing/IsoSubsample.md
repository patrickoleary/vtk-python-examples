### Description

This example demonstrates aliasing that occurs when a high-frequency signal is subsampled. The left viewport shows an isosurface of the skull after subsampling (aliased stair-stepping edges). The right viewport shows the same isosurface after a low-pass Gaussian filter before subsampling, which eliminates the aliasing. It follows the VTK pipeline structure:

**Reader → ImageShrink3D → ImageMarchingCubes → PolyDataMapper → Actor (left — aliased)**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) represents the isosurface in the scene.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) applies a low-pass filter before subsampling to reduce high-frequency energy.
- [vtkImageMarchingCubes](https://www.vtk.org/doc/nightly/html/classvtkImageMarchingCubes.html) extracts an isosurface at intensity value 1150.
- [vtkImageShrink3D](https://www.vtk.org/doc/nightly/html/classvtkImageShrink3D.html) subsamples the volume by a factor of 4 in X and Y.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the isosurface polygons to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
