#!/usr/bin/env python

# Create four 2D cursors with different configurations using vtkCursor2D.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkCursor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Cursor 1: axes + outline
cursor = vtkCursor2D()
cursor.SetModelBounds(15, 45, 15, 45, 0, 0)
cursor.SetFocalPoint(30, 30, 0)
cursor.AllOff()
cursor.AxesOn()
cursor.OutlineOn()

cursor_mapper = vtkPolyDataMapper2D()
cursor_mapper.SetInputConnection(cursor.GetOutputPort())

cursor_actor = vtkActor2D()
cursor_actor.SetMapper(cursor_mapper)
cursor_actor.GetProperty().SetColor(1, 0, 0)

# Cursor 2: axes + outline + point
cursor_2 = vtkCursor2D()
cursor_2.SetModelBounds(75, 105, 15, 45, 0, 0)
cursor_2.SetFocalPoint(90, 30, 0)
cursor_2.AllOff()
cursor_2.AxesOn()
cursor_2.OutlineOn()
cursor_2.PointOn()

cursor_2_mapper = vtkPolyDataMapper2D()
cursor_2_mapper.SetInputConnection(cursor_2.GetOutputPort())

cursor_2_actor = vtkActor2D()
cursor_2_actor.SetMapper(cursor_2_mapper)
cursor_2_actor.GetProperty().SetColor(0, 1, 0)

# Cursor 3: axes + point with radius, no outline
cursor_3 = vtkCursor2D()
cursor_3.SetModelBounds(15, 45, 75, 105, 0, 0)
cursor_3.SetFocalPoint(30, 90, 0)
cursor_3.AllOff()
cursor_3.AxesOn()
cursor_3.OutlineOff()
cursor_3.PointOn()
cursor_3.SetRadius(3)

cursor_3_mapper = vtkPolyDataMapper2D()
cursor_3_mapper.SetInputConnection(cursor_3.GetOutputPort())

cursor_3_actor = vtkActor2D()
cursor_3_actor.SetMapper(cursor_3_mapper)
cursor_3_actor.GetProperty().SetColor(0, 1, 0)

# Cursor 4: axes only with zero radius
cursor_4 = vtkCursor2D()
cursor_4.SetModelBounds(75, 105, 75, 105, 0, 0)
cursor_4.SetFocalPoint(90, 90, 0)
cursor_4.AllOff()
cursor_4.AxesOn()
cursor_4.SetRadius(0.0)

cursor_4_mapper = vtkPolyDataMapper2D()
cursor_4_mapper.SetInputConnection(cursor_4.GetOutputPort())

cursor_4_actor = vtkActor2D()
cursor_4_actor.SetMapper(cursor_4_mapper)
cursor_4_actor.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cursor_actor)
renderer.AddActor(cursor_2_actor)
renderer.AddActor(cursor_3_actor)
renderer.AddActor(cursor_4_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(150, 150)
render_window.SetMultiSamples(0)
render_window.SetWindowName("cursor2d")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
