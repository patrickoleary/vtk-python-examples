#!/usr/bin/env python

# Test vtkLeaderActor2D with various arrow styles and label configurations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkRenderingAnnotation import vtkLeaderActor2D
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Filled arrow style
leader = vtkLeaderActor2D()
leader.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
leader.GetPositionCoordinate().SetValue(0.1, 0.1)
leader.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
leader.GetPosition2Coordinate().SetValue(0.75, 0.23)
leader.SetArrowStyleToFilled()
leader.SetLabel("")

# Open arrow at point1
leader_2 = vtkLeaderActor2D()
leader_2.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
leader_2.GetPositionCoordinate().SetValue(0.9, 0.1)
leader_2.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
leader_2.GetPosition2Coordinate().SetValue(0.75, 0.83)
leader_2.SetArrowStyleToOpen()
leader_2.SetArrowPlacementToPoint1()
leader_2.SetLabel("Leader2")

# Hollow arrow
leader_3 = vtkLeaderActor2D()
leader_3.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
leader_3.GetPositionCoordinate().SetValue(0.1, 0.9)
leader_3.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
leader_3.GetPosition2Coordinate().SetValue(0.6, 0.3)
leader_3.SetArrowStyleToHollow()
leader_3.SetLabel("Leader3")

# No arrow, auto label
leader_4 = vtkLeaderActor2D()
leader_4.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
leader_4.GetPositionCoordinate().SetValue(0.1, 0.75)
leader_4.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
leader_4.GetPosition2Coordinate().SetValue(0.1, 0.25)
leader_4.SetArrowPlacementToNone()
leader_4.SetRadius(1.0)
leader_4.SetLabel("Leader4")
leader_4.AutoLabelOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(leader)
renderer.AddActor(leader_2)
renderer.AddActor(leader_3)
renderer.AddActor(leader_4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("leader actor2d")
render_window.SetMultiSamples(0)
render_window.SetSize(250, 250)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
