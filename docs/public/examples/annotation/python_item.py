#!/usr/bin/env python

# Demonstrate vtkPythonItem for custom 2D drawing with Context2D API.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkRectd,
    vtkRecti,
)
from vtkmodules.vtkChartsCore import vtkAxis, vtkInteractiveArea
from vtkmodules.vtkPythonContext2D import vtkPythonItem
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkMarkerUtilities
from vtkmodules.vtkRenderingCore import (
    VTK_SCALAR_MODE_USE_CELL_DATA,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)

# Build polydata with a single colored line
pts = vtkPoints()
pts.InsertNextPoint([0.1, 0.1, 0.0])
pts.InsertNextPoint([0.9, 0.9, 0.0])

lines = vtkCellArray()
lines.InsertNextCell(2)
lines.InsertCellPoint(0)
lines.InsertCellPoint(1)

colors = vtkUnsignedCharArray()
colors.SetNumberOfComponents(4)
colors.InsertNextTypedTuple([27, 128, 89, 255])

polydata = vtkPolyData()
polydata.SetPoints(pts)
polydata.SetLines(lines)
polydata.GetCellData().SetScalars(colors)


# Custom Python item for 2D drawing
class CustomPythonItem:
    def __init__(self, pd):
        self.polydata = pd

    def Initialize(self, vtk_self):
        return True

    def Paint(self, vtk_self, context_2d):
        # Draw the polydata line
        context_2d.DrawPolyData(
            0.0, 0.0, self.polydata,
            self.polydata.GetCellData().GetScalars(),
            VTK_SCALAR_MODE_USE_CELL_DATA,
        )

        pen = context_2d.GetPen()
        pen_color = [0, 0, 0]
        pen.GetColor(pen_color)
        pen_width = pen.GetWidth()

        brush = context_2d.GetBrush()
        brush_color = [0, 0, 0, 0]
        brush.GetColor(brush_color)

        # Blue wedge
        pen.SetColor([0, 0, 255])
        brush.SetColor([0, 0, 255])
        context_2d.DrawWedge(0.75, 0.25, 0.125, 0.005, 30.0, 60.0)

        # Black circle markers
        pen.SetWidth(20.0)
        pen.SetColor([0, 0, 0])
        brush.SetColor([0, 0, 0])
        context_2d.DrawMarkers(
            vtkMarkerUtilities.CIRCLE, False,
            [0.1, 0.1, 0.5, 0.5, 0.9, 0.9], 3,
        )
        pen.SetWidth(1.0)

        # Rotated text
        text_prop = vtkTextProperty()
        text_prop.BoldOn()
        text_prop.ItalicOn()
        text_prop.SetFontSize(22)
        text_prop.SetColor(0.5, 0.0, 1.0)
        text_prop.SetOrientation(45)
        context_2d.ApplyTextProp(text_prop)
        context_2d.DrawString(0.35, 0.4, "Context2D!")

        # Yellow semi-transparent polygon
        pen.SetColor([200, 200, 30])
        brush.SetColor([200, 200, 30])
        brush.SetOpacity(128)
        context_2d.DrawPolygon([0.5, 0.5, 0.75, 0.0, 1.0, 0.5], 3)

        # Brown filled arc
        pen.SetColor([133, 70, 70])
        brush.SetColor([133, 70, 70])
        brush.SetOpacity(255)
        context_2d.DrawArc(0.25, 0.75, 0.125, 0.0, 360.0)

        # Restore pen and brush state
        pen.SetWidth(pen_width)
        pen.SetColor(pen_color)
        brush.SetColor(brush_color[:3])
        brush.SetOpacity(brush_color[3])

        return True


# Set up the interactive area with axes hidden
width = 400
height = 400

area = vtkInteractiveArea()

draw_area_bounds = vtkRectd(0.0, 0.0, 1.0, 1.0)

vp = [0.05, 0.95, 0.05, 0.95]
screen_geometry = vtkRecti(
    int(vp[0] * width),
    int(vp[2] * height),
    int((vp[1] - vp[0]) * width),
    int((vp[3] - vp[2]) * height),
)

item = vtkPythonItem()
item.SetPythonObject(CustomPythonItem(polydata))
item.SetVisible(True)
area.GetDrawAreaItem().AddItem(item)

area.SetDrawAreaBounds(draw_area_bounds)
area.SetGeometry(screen_geometry)
area.SetFillViewport(False)
area.SetShowGrid(False)

# Hide all axes
ax_left = area.GetAxis(vtkAxis.LEFT)
ax_left.SetVisible(False)
ax_left.SetMargins(0, 0)
ax_right = area.GetAxis(vtkAxis.RIGHT)
ax_right.SetVisible(False)
ax_right.SetMargins(0, 0)
ax_bottom = area.GetAxis(vtkAxis.BOTTOM)
ax_bottom.SetVisible(False)
ax_bottom.SetMargins(0, 0)
ax_top = area.GetAxis(vtkAxis.TOP)
ax_top.SetVisible(False)
ax_top.SetMargins(0, 0)

# Use vtkContextActor
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(area)

renderer = vtkRenderer()
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

render_window = vtkRenderWindow()
render_window.SetSize(width, height)
render_window.AddRenderer(renderer)
render_window.SetWindowName("python item")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
