### Description

This example demonstrates edge-preserving smoothing of a 3D medical volume (FullHead.mhd) using vtkImageAnisotropicDiffusion2D. The left viewport shows the original middle axial slice of a CT head scan with typical noise and graininess; the right shows the diffused result where flat regions (soft tissue, air cavities) appear smoother and more uniform while sharp edges (skull boundaries, tissue interfaces) are preserved. This is the hallmark of anisotropic diffusion — it smooths along surfaces but not across boundaries. It follows the VTK pipeline structure:

**Reader → AnisotropicDiffusion2D → ImageCast → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays a 2D slice. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageAnisotropicDiffusion2D](https://www.vtk.org/doc/nightly/html/classvtkImageAnisotropicDiffusion2D.html) performs edge-preserving smoothing. `SetNumberOfIterations()` controls how much smoothing is applied. `SetDiffusionThreshold()` limits diffusion across edges with gradients above this value.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display. `ClampOverflowOn()` prevents wrap-around artifacts.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume (256×256×94 voxels of signed short scalars).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout for comparison.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
