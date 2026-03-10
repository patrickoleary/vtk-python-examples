### Description

This example reads an STL mesh, voxelizes it into a binary stencil mask, writes the mask to a VTK XML ImageData (.vti) file, reads it back, and visualizes the center slice alongside the original mesh.

**STL Reader → Stencil → VTI Writer → VTI Reader → Visualization**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) overlays the original STL mesh with semi-transparency.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the center Z-slice of the read-back voxelized mask.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) creates a blank volume covering the mesh bounding box with padding. `AllocateScalars()` initializes the voxel grid with zeros.
- [vtkImageStencil](https://www.vtk.org/doc/nightly/html/classvtkImageStencil.html) applies the stencil to the blank image, producing a binary mask. `ReverseStencilOn()` fills interior voxels.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkPolyDataToImageStencil](https://www.vtk.org/doc/nightly/html/classvtkPolyDataToImageStencil.html) converts the polydata surface into a stencil marking which voxels are inside or outside the mesh.
- [vtkSTLReader](https://www.vtk.org/doc/nightly/html/classvtkSTLReader.html) reads a stereolithography (.stl) file. `SetFileName()` specifies the input mesh.
- [vtkXMLImageDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLImageDataReader.html) reads the written VTI file back, verifying the round-trip.
- [vtkXMLImageDataWriter](https://www.vtk.org/doc/nightly/html/classvtkXMLImageDataWriter.html) writes the voxelized mask to a VTK XML ImageData (.vti) file. VTI is VTK's native XML format for structured image data.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
