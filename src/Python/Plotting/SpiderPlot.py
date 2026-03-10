#!/usr/bin/env python

# Spider (radar) plot of random food-texture data using vtkSpiderPlotActor.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMinimalStandardRandomSequence,
)
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkRenderingAnnotation import vtkSpiderPlotActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)
misty_rose_rgb = (1.0, 0.894, 0.882)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Data: five food-texture attributes with random values
num_tuples = 12

bitter = vtkFloatArray()
bitter.SetNumberOfTuples(num_tuples)

crispy = vtkFloatArray()
crispy.SetNumberOfTuples(num_tuples)

crunchy = vtkFloatArray()
crunchy.SetNumberOfTuples(num_tuples)

salty = vtkFloatArray()
salty.SetNumberOfTuples(num_tuples)

oily = vtkFloatArray()
oily.SetNumberOfTuples(num_tuples)

rand_seq = vtkMinimalStandardRandomSequence()
rand_seq.SetSeed(8775070)

for i in range(num_tuples):
    bitter.SetTuple1(i, rand_seq.GetRangeValue(1, 10))
    rand_seq.Next()
    crispy.SetTuple1(i, rand_seq.GetRangeValue(-1, 1))
    rand_seq.Next()
    crunchy.SetTuple1(i, rand_seq.GetRangeValue(1, 100))
    rand_seq.Next()
    salty.SetTuple1(i, rand_seq.GetRangeValue(0, 10))
    rand_seq.Next()
    oily.SetTuple1(i, rand_seq.GetRangeValue(5, 25))
    rand_seq.Next()

data_object = vtkDataObject()
data_object.GetFieldData().AddArray(bitter)
data_object.GetFieldData().AddArray(crispy)
data_object.GetFieldData().AddArray(crunchy)
data_object.GetFieldData().AddArray(salty)
data_object.GetFieldData().AddArray(oily)

# SpiderPlotActor: radar chart displaying all five axes
spider = vtkSpiderPlotActor()
spider.SetInputData(data_object)
spider.SetTitle("Spider Plot")
spider.SetIndependentVariablesToColumns()
spider.GetPositionCoordinate().SetValue(0.05, 0.1, 0.0)
spider.GetPosition2Coordinate().SetValue(0.95, 0.85, 0.0)
spider.GetProperty().SetColor(red_rgb)

spider.SetAxisLabel(0, "Bitter")
spider.SetAxisRange(0, 1, 10)
spider.SetAxisLabel(1, "Crispy")
spider.SetAxisRange(1, -1, 1)
spider.SetAxisLabel(2, "Crunchy")
spider.SetAxisRange(2, 1, 100)
spider.SetAxisLabel(3, "Salty")
spider.SetAxisRange(3, 0, 10)
spider.SetAxisLabel(4, "Oily")
spider.SetAxisRange(4, 5, 25)

spider.GetLegendActor().SetNumberOfEntries(num_tuples)
for i in range(num_tuples):
    r = rand_seq.GetRangeValue(0.4, 1.0)
    rand_seq.Next()
    g = rand_seq.GetRangeValue(0.4, 1.0)
    rand_seq.Next()
    b = rand_seq.GetRangeValue(0.4, 1.0)
    rand_seq.Next()
    spider.SetPlotColor(i, r, g, b)

spider.LegendVisibilityOn()
spider.GetTitleTextProperty().SetColor(misty_rose_rgb)
spider.GetLabelTextProperty().SetColor(misty_rose_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(spider)
renderer.SetBackground(dark_slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SpiderPlot")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
