### Description

This example classifies cells of a cow mesh as inside, outside, or on the border of a rotated copy using vtkSelectEnclosedPoints and vtkMultiThreshold. Outside cells are crimson, inside cells are yellow, and border cells are green. A translucent copy of the closed surface illustrates the selection.

**Reader → Transform → SelectEnclosedPoints → MultiThreshold → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) displays each cell classification in a distinct colour.
- [vtkDataObject](https://www.vtk.org/doc/nightly/html/classvtkDataObject.html) provides field association constants used by vtkMultiThreshold.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the classified cell sets to graphics primitives.
- [vtkMultiThreshold](https://www.vtk.org/doc/nightly/html/classvtkMultiThreshold.html) extracts inside, outside, and border cell sets into separate blocks.
- [vtkSelectEnclosedPoints](https://www.vtk.org/doc/nightly/html/classvtkSelectEnclosedPoints.html) marks points that are inside or outside the closed surface.
- [vtkTransform](https://www.vtk.org/doc/nightly/html/classvtkTransform.html) rotates the cow 90 degrees about Y to create the enclosing surface.
- [vtkTransformPolyDataFilter](https://www.vtk.org/doc/nightly/html/classvtkTransformPolyDataFilter.html) applies the rotation transform to the cow mesh.
- [vtkXMLPolyDataReader](https://www.vtk.org/doc/nightly/html/classvtkXMLPolyDataReader.html) loads the cow mesh from a `.vtp` file.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
