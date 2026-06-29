#!/usr/bin/env python

# Layout a simple graph in 2D and 3D using vtkGraphLayoutFilter, displaying
# edges as tubes and vertices as sphere glyphs.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkGlyph3D,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkGraphLayoutFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()

# Create a simple graph (jittered from optimum)
pts = vtkPoints()
pts.SetNumberOfPoints(10)
pts.SetPoint(0, -0.5, 1.0, -0.3)
pts.SetPoint(1, -3.0, 0.1, 0.2)
pts.SetPoint(2, 0.0, 0.0, 0.0)
pts.SetPoint(3, 1.2, -0.1, -0.2)
pts.SetPoint(4, 0.2, -3.0, 0.2)
pts.SetPoint(5, -4.2, -5.5, 0.7)
pts.SetPoint(6, 1.2, -7.3, -0.6)
pts.SetPoint(7, 4.2, -5.5, 0.7)
pts.SetPoint(8, 0.0, 0.0, -0.4)
pts.SetPoint(9, 0.0, 0.0, 0.8)

lines = vtkCellArray()
lines.InsertNextCell(4)
lines.InsertCellPoint(0)
lines.InsertCellPoint(2)
lines.InsertCellPoint(4)
lines.InsertCellPoint(6)
lines.InsertNextCell(2)
lines.InsertCellPoint(1)
lines.InsertCellPoint(2)
lines.InsertNextCell(2)
lines.InsertCellPoint(2)
lines.InsertCellPoint(3)
lines.InsertNextCell(2)
lines.InsertCellPoint(5)
lines.InsertCellPoint(6)
lines.InsertNextCell(2)
lines.InsertCellPoint(6)
lines.InsertCellPoint(7)
lines.InsertNextCell(2)
lines.InsertCellPoint(2)
lines.InsertCellPoint(8)
lines.InsertNextCell(2)
lines.InsertCellPoint(2)
lines.InsertCellPoint(9)

pd = vtkPolyData()
pd.SetPoints(pts)
pd.SetLines(lines)

# 2D layout
layout_2d = vtkGraphLayoutFilter()
layout_2d.SetInputData(pd)
layout_2d.SetMaxNumberOfIterations(100)
layout_2d.ThreeDimensionalLayoutOff()
layout_2d.AutomaticBoundsComputationOff()
layout_2d.SetGraphBounds(-2.0, 0.0, -1.0, 1.0, -1.0, 1.0)

# 3D layout
layout_3d = vtkGraphLayoutFilter()
layout_3d.SetInputData(pd)
layout_3d.SetMaxNumberOfIterations(100)
layout_3d.ThreeDimensionalLayoutOn()
layout_3d.AutomaticBoundsComputationOff()
layout_3d.SetGraphBounds(0.0, 2.0, -1.0, 1.0, -1.0, 1.0)

# Append both layouts
apf = vtkAppendPolyData()
apf.AddInputConnection(layout_2d.GetOutputPort())
apf.AddInputConnection(layout_3d.GetOutputPort())

# Edge tubes
tubes = vtkTubeFilter()
tubes.SetInputConnection(apf.GetOutputPort())
tubes.SetRadius(0.01)
tubes.SetNumberOfSides(6)

edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(tubes.GetOutputPort())

peacock_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("peacock", peacock_rgb)
hot_pink_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("hot_pink", hot_pink_rgb)

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(peacock_rgb)
edge_actor.GetProperty().SetSpecularColor(1, 1, 1)
edge_actor.GetProperty().SetSpecular(0.3)
edge_actor.GetProperty().SetSpecularPower(20)
edge_actor.GetProperty().SetAmbient(0.2)
edge_actor.GetProperty().SetDiffuse(0.8)

# Vertex glyphs
ball = vtkSphereSource()
ball.SetRadius(0.025)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)

balls = vtkGlyph3D()
balls.SetInputConnection(apf.GetOutputPort())
balls.SetSourceConnection(ball.GetOutputPort())

ball_mapper = vtkPolyDataMapper()
ball_mapper.SetInputConnection(balls.GetOutputPort())

ball_actor = vtkActor()
ball_actor.SetMapper(ball_mapper)
ball_actor.GetProperty().SetColor(hot_pink_rgb)
ball_actor.GetProperty().SetSpecularColor(1, 1, 1)
ball_actor.GetProperty().SetSpecular(0.3)
ball_actor.GetProperty().SetSpecularPower(20)
ball_actor.GetProperty().SetAmbient(0.2)
ball_actor.GetProperty().SetDiffuse(0.8)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(ball_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 250)
render_window.SetWindowName("graph layout")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetClippingRange(3.55085, 6.01004)
cam.SetFocalPoint(0.0427, -0.0149608, 0.0)
cam.SetPosition(0.0427, -0.0149608, 4.63462)
cam.SetViewUp(0, 1, 0)

interactor.Initialize()
interactor.Start()
