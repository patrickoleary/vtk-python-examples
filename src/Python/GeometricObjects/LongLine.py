#!/usr/bin/env python

# Connect several points with line segments using vtkLine cells.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock_rgb = (0.2, 0.631, 0.788)
silver_background_rgb = (0.75, 0.75, 0.75)

# Data: five points forming a path
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 2.0)
points.InsertNextPoint(1.0, 2.0, 3.0)

# Cells: three line segments connecting consecutive points
lines = vtkCellArray()

line0 = vtkLine()
line0.GetPointIds().SetId(0, 0)
line0.GetPointIds().SetId(1, 1)
lines.InsertNextCell(line0)

line1 = vtkLine()
line1.GetPointIds().SetId(0, 1)
line1.GetPointIds().SetId(1, 2)
lines.InsertNextCell(line1)

line2 = vtkLine()
line2.GetPointIds().SetId(0, 2)
line2.GetPointIds().SetId(1, 3)
lines.InsertNextCell(line2)

# Assemble the polydata
lines_poly_data = vtkPolyData()
lines_poly_data.SetPoints(points)
lines_poly_data.SetLines(lines)

# Mapper: map line polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(lines_poly_data)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(4)
actor.GetProperty().SetColor(peacock_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(silver_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("LongLine")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
