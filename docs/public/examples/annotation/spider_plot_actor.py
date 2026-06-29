#!/usr/bin/env python

# Test vtkSpiderPlotActor with multiple random data arrays and colored plots.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkRenderingAnnotation import vtkSpiderPlotActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

num_tuples = 12

# Fixed data arrays
bitter = vtkFloatArray()
bitter.SetNumberOfTuples(num_tuples)
for i, v in enumerate([3.2, 7.1, 5.4, 2.8, 9.0, 4.6, 6.3, 1.5, 8.7, 3.9, 5.1, 7.8]):
    bitter.SetTuple1(i, v)

crispy = vtkFloatArray()
crispy.SetNumberOfTuples(num_tuples)
for i, v in enumerate([0.3, -0.5, 0.8, -0.2, 0.6, -0.9, 0.1, 0.7, -0.4, 0.5, -0.1, 0.9]):
    crispy.SetTuple1(i, v)

crunchy = vtkFloatArray()
crunchy.SetNumberOfTuples(num_tuples)
for i, v in enumerate([45.2, 12.8, 78.3, 33.1, 91.5, 56.7, 23.4, 67.9, 8.6, 84.2, 41.0, 59.3]):
    crunchy.SetTuple1(i, v)

salty = vtkFloatArray()
salty.SetNumberOfTuples(num_tuples)
for i, v in enumerate([2.1, 8.4, 5.7, 1.3, 6.9, 3.5, 9.2, 4.8, 7.6, 0.9, 5.3, 2.7]):
    salty.SetTuple1(i, v)

oily = vtkFloatArray()
oily.SetNumberOfTuples(num_tuples)
for i, v in enumerate([12.3, 18.7, 8.5, 22.1, 15.4, 9.8, 20.6, 14.2, 7.9, 23.5, 11.1, 16.8]):
    oily.SetTuple1(i, v)

data_object = vtkDataObject()
data_object.GetFieldData().AddArray(bitter)
data_object.GetFieldData().AddArray(crispy)
data_object.GetFieldData().AddArray(crunchy)
data_object.GetFieldData().AddArray(salty)
data_object.GetFieldData().AddArray(oily)

# Spider plot actor
spider_plot_actor = vtkSpiderPlotActor()
spider_plot_actor.SetInputData(data_object)
spider_plot_actor.SetTitle("Spider Plot")
spider_plot_actor.SetIndependentVariablesToColumns()
spider_plot_actor.GetPositionCoordinate().SetValue(0.05, 0.1, 0.0)
spider_plot_actor.GetPosition2Coordinate().SetValue(0.95, 0.85, 0.0)
spider_plot_actor.GetProperty().SetColor(1, 0, 0)
spider_plot_actor.SetAxisLabel(0, "Bitter")
spider_plot_actor.SetAxisRange(0, 1, 10)
spider_plot_actor.SetAxisLabel(1, "Crispy")
spider_plot_actor.SetAxisRange(1, -1, 1)
spider_plot_actor.SetAxisLabel(2, "Crunchy")
spider_plot_actor.SetAxisRange(2, 1, 100)
spider_plot_actor.SetAxisLabel(3, "Salty")
spider_plot_actor.SetAxisRange(3, 0, 10)
spider_plot_actor.SetAxisLabel(4, "Oily")
spider_plot_actor.SetAxisRange(4, 5, 25)
spider_plot_actor.GetLegendActor().SetNumberOfEntries(num_tuples)

spider_plot_actor.SetPlotColor(0, 0.85, 0.23, 0.12)
spider_plot_actor.SetPlotColor(1, 0.14, 0.72, 0.31)
spider_plot_actor.SetPlotColor(2, 0.42, 0.18, 0.91)
spider_plot_actor.SetPlotColor(3, 0.67, 0.55, 0.08)
spider_plot_actor.SetPlotColor(4, 0.29, 0.44, 0.76)
spider_plot_actor.SetPlotColor(5, 0.93, 0.37, 0.52)
spider_plot_actor.SetPlotColor(6, 0.11, 0.63, 0.48)
spider_plot_actor.SetPlotColor(7, 0.78, 0.21, 0.65)
spider_plot_actor.SetPlotColor(8, 0.35, 0.82, 0.14)
spider_plot_actor.SetPlotColor(9, 0.56, 0.09, 0.88)
spider_plot_actor.SetPlotColor(10, 0.44, 0.71, 0.33)
spider_plot_actor.SetPlotColor(11, 0.19, 0.45, 0.72)

spider_plot_actor.LegendVisibilityOn()
spider_plot_actor.GetTitleTextProperty().SetColor(1, 1, 0)
spider_plot_actor.GetLabelTextProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(spider_plot_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("spider plot actor")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
