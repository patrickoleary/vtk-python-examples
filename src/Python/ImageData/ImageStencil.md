### Description

This example masks a region of a 3D medical volume using vtkImageStencil. A spherical binary mask is generated with vtkImageEllipsoidSource and converted to a stencil via vtkImageToImageStencil. Only voxels inside the ellipsoid are kept; everything outside is set to zero. It follows the VTK pipeline structure:

**Reader + ImageEllipsoidSource → ImageToImageStencil → ImageStencil → ImageCast → ImageActor → Renderer → Window → Interactor**

- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the middle axial slice of the masked volume.
- [vtkImageCast](https://www.vtk.org/doc/nightly/html/classvtkImageCast.html) converts the masked output to unsigned char for display.
- [vtkImageEllipsoidSource](https://www.vtk.org/doc/nightly/html/classvtkImageEllipsoidSource.html) generates a binary mask image with an ellipsoidal region. `SetCenter()` places the ellipsoid at the volume center. `SetRadius()` defines the semi-axes. `SetInValue(255)` and `SetOutValue(0)` create a binary mask.
- [vtkImageStencil](https://www.vtk.org/doc/nightly/html/classvtkImageStencil.html) applies the stencil mask. Voxels inside the ellipsoid are kept; voxels outside are replaced with `SetBackgroundValue(0)`.
- [vtkImageToImageStencil](https://www.vtk.org/doc/nightly/html/classvtkImageToImageStencil.html) converts the binary mask image into an image stencil. `ThresholdByUpper(128)` treats mask values ≥ 128 as the region to keep.
- [vtkMetaImageReader](https://www.vtk.org/doc/nightly/html/classvtkMetaImageReader.html) reads the `FullHead.mhd` MetaImage volume (256×256×94 voxels of signed short scalars).
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a black background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
