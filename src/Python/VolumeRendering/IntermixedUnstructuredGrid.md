### Description

This example intermixeds rendering of an unstructured grid volume with a polygonal contour surface. The iron protein dataset is volume rendered while the neghip dataset is displayed as a polygonal isosurface, both in the same scene.

**StructuredPointsReader → Threshold → Triangulate → UnstructuredGridVolumeMapper → Volume**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped contour geometry.
- [vtkColorTransferFunction](https://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html) defines the scalar-to-color transfer function.
- [vtkContourFilter](https://www.vtk.org/doc/nightly/html/classvtkContourFilter.html) extracts a polygonal isosurface from the neghip data.
- [vtkDataSetTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkDataSetTriangleFilter.html) triangulates the unstructured grid for the ray cast mapper.
- [vtkNamedColors](https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html) provides named colors.
- [vtkPiecewiseFunction](https://www.vtk.org/doc/nightly/html/classvtkPiecewiseFunction.html) defines the scalar-to-opacity transfer function.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives.
- [vtkSLCReader](https://www.vtk.org/doc/nightly/html/classvtkSLCReader.html) reads the neghip SLC dataset for polygonal contouring.
- [vtkStructuredPointsReader](https://www.vtk.org/doc/nightly/html/classvtkStructuredPointsReader.html) reads the iron protein structured points dataset for volume rendering.
- [vtkThreshold](https://www.vtk.org/doc/nightly/html/classvtkThreshold.html) removes cells below a threshold to convert image data to unstructured grid.
- [vtkUnstructuredGridVolumeRayCastMapper](https://www.vtk.org/doc/nightly/html/classvtkUnstructuredGridVolumeRayCastMapper.html) performs ray casting on unstructured grid data.
- [vtkVolume](https://www.vtk.org/doc/nightly/html/classvtkVolume.html) holds the volume mapper and property.
- [vtkVolumeProperty](https://www.vtk.org/doc/nightly/html/classvtkVolumeProperty.html) describes shading and transfer functions for the volume.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
