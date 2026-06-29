#!/usr/bin/env python

# Test vtkPieChartActor with random data and colored slices.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkRenderingAnnotation import vtkPieChartActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

num_tuples = 6

# Fixed pie data
bitter = vtkFloatArray()
bitter.SetNumberOfTuples(num_tuples)
bitter.SetTuple1(0, 23.4)
bitter.SetTuple1(1, 67.1)
bitter.SetTuple1(2, 45.8)
bitter.SetTuple1(3, 89.2)
bitter.SetTuple1(4, 12.5)
bitter.SetTuple1(5, 56.3)

data_object = vtkDataObject()
data_object.GetFieldData().AddArray(bitter)

# Pie chart actor
pie_chart_actor = vtkPieChartActor()
pie_chart_actor.SetInputData(data_object)
pie_chart_actor.SetTitle("Pie Chart")
pie_chart_actor.GetPositionCoordinate().SetValue(0.05, 0.1, 0.0)
pie_chart_actor.GetPosition2Coordinate().SetValue(0.95, 0.85, 0.0)
pie_chart_actor.GetProperty().SetColor(0.1, 0.1, 0.1)
pie_chart_actor.GetLegendActor().SetNumberOfEntries(num_tuples)

pie_chart_actor.SetPieceColor(0, 0.85, 0.23, 0.12)
pie_chart_actor.SetPieceColor(1, 0.14, 0.72, 0.31)
pie_chart_actor.SetPieceColor(2, 0.42, 0.18, 0.91)
pie_chart_actor.SetPieceColor(3, 0.67, 0.55, 0.08)
pie_chart_actor.SetPieceColor(4, 0.29, 0.44, 0.76)
pie_chart_actor.SetPieceColor(5, 0.93, 0.37, 0.52)

pie_chart_actor.SetPieceLabel(0, "oil")
pie_chart_actor.SetPieceLabel(1, "gas")
pie_chart_actor.SetPieceLabel(2, "water")
pie_chart_actor.SetPieceLabel(3, "snake oil")
pie_chart_actor.SetPieceLabel(4, "tequila")
pie_chart_actor.SetPieceLabel(5, "beer")
pie_chart_actor.LegendVisibilityOn()

pie_chart_actor.GetTitleTextProperty().SetColor(1, 1, 0)
pie_chart_actor.GetLabelTextProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(pie_chart_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pie chart actor")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
