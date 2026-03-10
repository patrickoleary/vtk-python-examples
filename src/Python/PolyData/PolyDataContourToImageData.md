### Description

This example cuts a sphere to obtain a circle contour, extrude it, and use the extruded surface as a stencil to stamp a binary image, then display the result.

**Source → Cutter → Stripper → Extrusion → Stencil → ImageActor → Renderer → Window → Interactor**

- [vtkCutter](https://www.vtk.org/doc/nightly/html/classvtkCutter.html) cuts the sphere to produce a circular contour.
- [vtkImageActor](https://www.vtk.org/doc/nightly/html/classvtkImageActor.html) displays the resulting binary image.
- [vtkImageData](https://www.vtk.org/doc/nightly/html/classvtkImageData.html) holds the blank binary image that receives the stencil stamp.
- [vtkImageStencil](https://www.vtk.org/doc/nightly/html/classvtkImageStencil.html) applies the stencil to blank the image outside the contour.
- [vtkLinearExtrusionFilter](https://www.vtk.org/doc/nightly/html/classvtkLinearExtrusionFilter.html) extrudes the contour into a 3-D surface for stencil conversion.
- [vtkPlane](https://www.vtk.org/doc/nightly/html/classvtkPlane.html) defines the implicit cutting plane through the sphere.
- [vtkPolyDataToImageStencil](https://www.vtk.org/doc/nightly/html/classvtkPolyDataToImageStencil.html) converts the extruded polydata into a stencil.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates the input sphere polydata.
- [vtkStripper](https://www.vtk.org/doc/nightly/html/classvtkStripper.html) joins contour segments into a continuous polyline.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
