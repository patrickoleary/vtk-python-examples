### Description

This example computes a Euclidean distance transform from a binary mask of a 3D medical volume (FullHead.mhd) using vtkImageEuclideanDistance. The left viewport shows the original slice; the right shows the distance field mapped to a cool-to-warm colormap. The distance transform assigns each voxel the distance to the nearest boundary, useful for shape analysis and segmentation refinement. It follows the VTK pipeline structure:

**Reader → ImageThreshold → ImageEuclideanDistance → ImageMapToColors → ImageActor (right)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays 2D slices. `SetDisplayExtent()` selects the middle axial slice.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts image scalar type for display.
- [vtkImageEuclideanDistance](https://www.vtk.org/doc/nightly/html/classvtkImageEuclideanDistance.html) computes the Euclidean distance from each voxel to the nearest zero-valued voxel. `SetAlgorithmToSaito()` selects the efficient Saito algorithm.
- [vtkImageMapToColors](https://www.vtk.org/doc/nightly/html/classvtkImageMapToColors.html) applies the lookup table to produce a colored distance image.
- [vtkImageThreshold](https://www.vtk.org/doc/nightly/html/classvtkImageThreshold.html) creates a binary mask with `ThresholdByUpper(600)`.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps distance values to a blue-to-red colormap.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) — two renderers with `SetViewport()` create a left/right layout.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
