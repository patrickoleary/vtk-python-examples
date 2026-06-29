#!/usr/bin/env python

# Demonstrate vtkCompositePolyDataMapper with unaligned plane cut on multiblock data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet, vtkPlane
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create overlapping multiblock data
rt_source_1 = vtkRTAnalyticSource()
rt_source_1.SetWholeExtent(-2, 2, -2, 2, -2, 2)
rt_source_1.Update()

rt_source_2 = vtkRTAnalyticSource()
rt_source_2.SetWholeExtent(-2, 0, -2, 0, -2, 0)
rt_source_2.Update()

rt_source_3 = vtkRTAnalyticSource()
rt_source_3.SetWholeExtent(0, 2, -2, 0, -2, 0)
rt_source_3.Update()

multiblock = vtkMultiBlockDataSet()
multiblock.SetBlock(0, rt_source_1.GetOutputDataObject(0))
multiblock.SetBlock(1, rt_source_2.GetOutputDataObject(0))
multiblock.SetBlock(2, rt_source_3.GetOutputDataObject(0))

# Cut with an unaligned plane
cutter = vtkCutter()
cutter.SetInputData(multiblock)
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 0, 1)
cutter.SetCutFunction(plane)
cutter.Update()

# Map and render
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(cutter.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.5, 0.5, 0.5)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("batch order")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
