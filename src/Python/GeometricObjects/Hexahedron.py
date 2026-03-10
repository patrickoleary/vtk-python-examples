#!/usr/bin/env python

# Construct and render a hexahedron using vtkHexahedron.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkHexahedron,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
background_rgb = (0.2, 0.302, 0.4)

# Data: 8 vertices of a unit hexahedron (two faces in CCW order from outside)
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 0.0, 1.0)
points.InsertNextPoint(1.0, 0.0, 1.0)
points.InsertNextPoint(1.0, 1.0, 1.0)
points.InsertNextPoint(0.0, 1.0, 1.0)

# Cell: create a hexahedron referencing the 8 points
hexahedron = vtkHexahedron()
hexahedron.GetPointIds().SetId(0, 0)
hexahedron.GetPointIds().SetId(1, 1)
hexahedron.GetPointIds().SetId(2, 2)
hexahedron.GetPointIds().SetId(3, 3)
hexahedron.GetPointIds().SetId(4, 4)
hexahedron.GetPointIds().SetId(5, 5)
hexahedron.GetPointIds().SetId(6, 6)
hexahedron.GetPointIds().SetId(7, 7)

# Unstructured grid: store the hexahedron cell
unstructured_grid = vtkUnstructuredGrid()
unstructured_grid.SetPoints(points)
unstructured_grid.InsertNextCell(hexahedron.GetCellType(), hexahedron.GetPointIds())

# Mapper: map the unstructured grid to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(unstructured_grid)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Hexahedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
