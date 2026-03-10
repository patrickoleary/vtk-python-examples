### Description

This example compares two images using a checkerboard pattern with vtkImageCheckerboard. You should see a single CT head slice divided into a 4×4 grid of alternating tiles — sharp original tiles next to visibly blurry smoothed tiles. The contrast between crisp detail and soft blur makes differences easy to spot at tile boundaries. This technique is commonly used to evaluate image registration quality. It follows the VTK pipeline structure:

**Reader → ImageCast (original)**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the checkerboard as a 2D slice.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts data to unsigned char for display.
- [vtkImageCheckerboard](https://www.vtk.org/doc/nightly/html/classvtkImageCheckerboard.html) interleaves two images in a checkerboard pattern. `SetNumberOfDivisions(4, 4, 1)` creates a 4×4 grid of alternating tiles.
- [vtkImageGaussianSmooth](https://www.vtk.org/doc/nightly/html/classvtkImageGaussianSmooth.html) creates a smoothed version for comparison. `SetStandardDeviations()` and `SetRadiusFactors()` control the blur kernel.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a black background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
