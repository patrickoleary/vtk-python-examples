#!/usr/bin/env python

# Demonstrate vtkRegularPolygonSource by creating a closed polyline
# and a filled polygon side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Polyline (unfilled polygon outline)
polyline = vtkRegularPolygonSource()
polyline.SetCenter(1, 1, 1)
polyline.SetRadius(1)
polyline.SetNumberOfSides(12)
polyline.SetNormal(1, 2, 3)
polyline.GeneratePolylineOn()
polyline.GeneratePolygonOff()

polyline_mapper = vtkPolyDataMapper()
polyline_mapper.SetInputConnection(polyline.GetOutputPort())

polyline_actor = vtkActor()
polyline_actor.SetMapper(polyline_mapper)
polyline_actor.GetProperty().SetColor(0, 1, 0)
polyline_actor.GetProperty().SetAmbient(1)

# Filled polygon
polygon = vtkRegularPolygonSource()
polygon.SetCenter(3, 1, 1)
polygon.SetRadius(1)
polygon.SetNumberOfSides(12)
polygon.SetNormal(1, 2, 3)
polygon.GeneratePolylineOff()
polygon.GeneratePolygonOn()

polygon_mapper = vtkPolyDataMapper()
polygon_mapper.SetInputConnection(polygon.GetOutputPort())

polygon_actor = vtkActor()
polygon_actor.SetMapper(polygon_mapper)
polygon_actor.GetProperty().SetColor(1, 0, 0)
polygon_actor.GetProperty().SetAmbient(1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(polyline_actor)
renderer.AddActor(polygon_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("regular polygon source sides")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
