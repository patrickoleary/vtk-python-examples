### Description

This example extracts feature edges from a hyper tree grid using vtkHyperTreeGridFeatureEdges. The edges highlight boundaries between cells of different refinement levels, rendered in crimson over a translucent HTG surface for context. It follows the VTK pipeline structure:

**Source → FeatureEdges → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Two actors show the feature edges in crimson and the context wireframe.
- [vtkHyperTreeGridFeatureEdges](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridFeatureEdges.html) extracts edges at boundaries between cells of different refinement levels in the hyper tree grid. These edges reveal the adaptive mesh structure.
- [vtkHyperTreeGridGeometry](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridGeometry.html) extracts the external surface as a translucent wireframe for spatial context.
- [vtkHyperTreeGridSource](https://www.vtk.org/doc/nightly/html/classvtkHyperTreeGridSource.html) creates a hyper tree grid from a text descriptor with a `Depth` cell scalar field.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps the polydata to graphics primitives.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
