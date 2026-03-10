### Description

This example reads an STL mesh, voxelizes it into a binary stencil mask, writes the mask to a MetaImage (.mha) file, and visualizes the center slice alongside the original mesh.

**Reader → Blank Image → Stencil → Writer → Visualization**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) overlays the original STL mesh with semi-transparency so the stencil slice is visible inside.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the center Z-slice of the voxelized mask. `SetDisplayExtent()` selects the visible slice.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) creates a blank volume covering the mesh bounding box with padding. `AllocateScalars()` initializes the voxel grid with zeros.
- [vtkImageStencil](https://www.vtk.org/doc/nightly/html/classvtkImageStencil.html) applies the stencil to the blank image, filling interior voxels with a background value to produce a binary mask. `ReverseStencilOn()` inverts the stencil so that interior voxels are filled.
- [vtkMetaImageWriter](https://www.vtk.org/doc/nightly/html/classvtkMetaImageWriter.html) writes the voxelized mask to a MetaImage (.mha) file. MetaImage is a simple format widely used in medical imaging for volumetric data.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataToImageStencil](https://www.vtk.org/doc/nightly/html/classvtkPolyDataToImageStencil.html) converts the polydata surface into a stencil that marks which voxels are inside or outside the mesh. `SetOutputSpacing()`, `SetOutputOrigin()`, and `SetOutputWholeExtent()` align the stencil with the blank image.
- [vtkSTLReader](https://www.vtk.org/doc/nightly/html/classvtkSTLReader.html) reads a stereolithography (.stl) file. `SetFileName()` specifies the input mesh.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
