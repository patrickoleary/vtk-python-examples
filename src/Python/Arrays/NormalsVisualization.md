### Description

This example visualizes surface normals as arrow glyphs on a sphere, colored by the normal Z component to show directional variation. The semi-transparent sphere surface is visible underneath the glyph field.

**Sphere → Extract Normal Z → Arrow Glyphs → Lookup Table → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. The sphere actor uses `GetProperty().SetOpacity(0.4)` for semi-transparency and `SetBackfaceProperty()` for a distinct back-face color.
- [vtkArrowSource](https://www.vtk.org/doc/nightly/html/classvtkArrowSource.html) creates the arrow shape used for each glyph.
- [vtkFloatArray](https://www.vtk.org/doc/nightly/html/classvtkFloatArray.html) extracts the Z component of each surface normal into a custom scalar array. `GetPointData().GetNormals()` retrieves the normal vectors. `GetTuple3()` reads individual 3-component tuples.
- [vtkGlyph3D](https://www.vtk.org/doc/nightly/html/classvtkGlyph3D.html) places an arrow at each point, oriented along the surface normal. `SetVectorModeToUseNormal()` aligns glyphs with normals. `SetScaleFactor()` controls glyph size. `SetColorModeToColorByScalar()` maps the Z component to color.
- [vtkLookupTable](https://www.vtk.org/doc/nightly/html/classvtkLookupTable.html) maps normal Z values (-1 to 1) to a diverging blue-to-red color ramp.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps polygon data to graphics primitives. Two mappers are used — one for the arrow glyphs with scalar coloring and one for the sphere surface with `ScalarVisibilityOff()`.
- [vtkProperty](https://www.vtk.org/doc/nightly/html/classvtkProperty.html) defines a separate back-face material for the sphere. `SetColor()` sets the back-face color to tomato.
- [vtkSphereSource](https://www.vtk.org/doc/nightly/html/classvtkSphereSource.html) generates a sphere polygon mesh with computed normals.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene. `ResetCamera()` frames the data.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
