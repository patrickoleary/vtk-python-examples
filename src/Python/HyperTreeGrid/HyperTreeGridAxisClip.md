### Description

This example clips a hyper tree grid along an axis-aligned plane using vtkHyperTreeGridAxisClip. The filter removes cells on one side of the plane, keeping only the lower-X portion. The clipped surface is rendered colored by Depth with the full HTG wireframe shown as translucent context. It follows the VTK pipeline structure:

**Source → AxisClip → Geometry → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the clipped surface and the context wireframe.
- [vtkHyperTreeGridAxisClip](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridAxisClip.html) clips a hyper tree grid along an axis-aligned plane. `SetClipTypeToPlane()` selects planar clipping, `SetPlaneNormalAxis(0)` chooses the X axis, and `SetPlanePosition(2.0)` sets the cut location. `InsideOutOff()` keeps cells below the plane.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface of the HTG as polydata for rendering.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the surface polydata to graphics primitives. `SetScalarModeToUseCellFieldData()` and `SelectColorArray("Depth")` color by depth level.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
