### Description

This example masks a PNG image with a sphere stencil and a contour stencil, then display the two results side-by-side using vtkPolyDataToImageStencil.

**Reader → Stencil → ImageActor → Renderer → Window → Interactor**

- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) cuts the sphere to produce a circular contour.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the masked image results.
- [vtkImageAppend](https://www.vtk.org/doc/nightly/html/classvtkImageAppend.html) places the two masked images side-by-side.
- [vtkImageStencil](https://www.vtk.org/doc/nightly/html/classvtkImageStencil.html) applies each stencil to mask the image.
- [vtkPNGReader](https://www.vtk.org/doc/nightly/html/classvtkPNGReader.html) loads the input PNG image to be masked.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit cutting plane through the sphere.
- [vtkPolyDataToImageStencil](https://www.vtk.org/doc/nightly/html/classvtkPolyDataToImageStencil.html) converts the polydata shapes into image stencils.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the sphere used as one of the stencil shapes.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) joins contour segments into a continuous polyline.
- [vtkTriangleFilter](https://www.vtk.org/doc/nightly/html/classvtkTriangleFilter.html) triangulates the sphere for stencil conversion.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
