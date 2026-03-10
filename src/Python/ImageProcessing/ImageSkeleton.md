### Description

This example performs 2D skeletonization on a thresholded slice of a 3D medical volume (FullHead.mhd) using vtkImageSkeleton2D. The left viewport shows the binary threshold mask; the right shows the skeleton. Skeletonization thins the binary region to a 1-pixel-wide representation of its medial axis. It follows the VTK pipeline structure:

**Reader → ImageThreshold → ImageSkeleton2D → ImageActor (right viewport)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageSkeleton2D](https://www.vtk.org/doc/nightly/html/classvtkImageSkeleton2D.html) thins the binary mask to a 1-pixel-wide skeleton. `SetNumberOfIterations()` controls how many thinning passes are applied. `SetPrune(1)` removes short branches.
- [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html) creates a binary mask of bone-like intensities using `ThresholdByUpper(600)`.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
