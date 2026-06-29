#!/usr/bin/env python
# Demonstrate multiple scalars-to-colors items in separate chart viewports.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkChartXY,
    vtkColorTransferFunctionItem,
    vtkCompositeTransferFunctionItem,
    vtkLookupTableItem,
    vtkPiecewiseControlPointsItem,
    vtkPiecewiseFunctionItem,
)
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction, vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Lookup Table.
lookup_table = vtkLookupTable()
lookup_table.SetAlpha(0.5)
lookup_table.Build()

# Color transfer function.
color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddHSVSegment(0.0, 0.0, 1.0, 1.0, 0.3333, 0.3333, 1.0, 1.0)
color_transfer_function.AddHSVSegment(0.3333, 0.3333, 1.0, 1.0, 0.6666, 0.6666, 1.0, 1.0)
color_transfer_function.AddHSVSegment(0.6666, 0.6666, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0)
color_transfer_function.Build()

# Opacity function.
opacity_function = vtkPiecewiseFunction()
opacity_function.AddPoint(0.0, 0.0)
opacity_function.AddPoint(1.0, 1.0)

# Histogram table.
histo_table = vtkTable()
bin_array = vtkDoubleArray()
bin_array.SetName("bins")
histo_table.AddColumn(bin_array)
value_array = vtkDoubleArray()
value_array.SetName("values")
histo_table.AddColumn(value_array)

histo_table.SetNumberOfRows(3)
histo_table.SetValue(0, 0, 0.25)
histo_table.SetValue(0, 1, 2)
histo_table.SetValue(1, 0, 0.5)
histo_table.SetValue(1, 1, 5)
histo_table.SetValue(2, 0, 0.75)
histo_table.SetValue(2, 1, 8)

# Chart 0 — vtkLookupTable.
chart_0 = vtkChartXY()
chart_scene_0 = vtkContextScene()
chart_scene_0.AddItem(chart_0)
chart_actor_0 = vtkContextActor()
chart_actor_0.SetScene(chart_scene_0)

lookup_table_item = vtkLookupTableItem()
lookup_table_item.SetLookupTable(lookup_table)
chart_0.AddPlot(lookup_table_item)
chart_0.SetAutoAxes(False)
chart_0.GetAxis(0).SetVisible(False)
chart_0.GetAxis(1).SetVisible(False)
chart_0.SetTitle("vtkLookupTable")

# Chart 1 — vtkColorTransferFunction.
chart_1 = vtkChartXY()
chart_scene_1 = vtkContextScene()
chart_scene_1.AddItem(chart_1)
chart_actor_1 = vtkContextActor()
chart_actor_1.SetScene(chart_scene_1)

color_transfer_function_item = vtkColorTransferFunctionItem()
color_transfer_function_item.SetColorTransferFunction(color_transfer_function)
color_transfer_function_item.SetOpacity(0.8)
chart_1.AddPlot(color_transfer_function_item)
chart_1.SetTitle("vtkColorTransferFunction")

# Chart 2 — vtkColorTransferFunction + vtkPiecewiseFunction.
chart_2 = vtkChartXY()
chart_scene_2 = vtkContextScene()
chart_scene_2.AddItem(chart_2)
chart_actor_2 = vtkContextActor()
chart_actor_2.SetScene(chart_scene_2)

composite_item_0 = vtkCompositeTransferFunctionItem()
composite_item_0.SetColorTransferFunction(color_transfer_function)
composite_item_0.SetOpacityFunction(opacity_function)
composite_item_0.SetMaskAboveCurve(True)
chart_2.AddPlot(composite_item_0)
chart_2.SetTitle("vtkColorTransferFunction + vtkPiecewiseFunction")

# Chart 3 — vtkPiecewiseFunction.
chart_3 = vtkChartXY()
chart_scene_3 = vtkContextScene()
chart_scene_3.AddItem(chart_3)
chart_actor_3 = vtkContextActor()
chart_actor_3.SetScene(chart_scene_3)

piecewise_function_item = vtkPiecewiseFunctionItem()
piecewise_function_item.SetPiecewiseFunction(opacity_function)
piecewise_function_item.SetColorF(1.0, 0, 0)
chart_3.AddPlot(piecewise_function_item)
control_points_item = vtkPiecewiseControlPointsItem()
control_points_item.SetPiecewiseFunction(opacity_function)
chart_3.AddPlot(control_points_item)
chart_3.SetTitle("vtkPiecewiseFunction")

# Chart 4 — histogramTable.
chart_4 = vtkChartXY()
chart_scene_4 = vtkContextScene()
chart_scene_4.AddItem(chart_4)
chart_actor_4 = vtkContextActor()
chart_actor_4.SetScene(chart_scene_4)

composite_item_1 = vtkCompositeTransferFunctionItem()
composite_item_1.SetColorTransferFunction(color_transfer_function)
composite_item_1.SetOpacityFunction(opacity_function)
composite_item_1.SetHistogramTable(histo_table)
composite_item_1.SetMaskAboveCurve(True)
chart_4.AddPlot(composite_item_1)
chart_4.SetTitle("histogramTable")

# Renderers.
renderer_0 = vtkRenderer()
renderer_0.SetBackground(1.0, 1.0, 1.0)
renderer_0.SetViewport(0.0, 0.0, 0.3, 0.5)
renderer_0.AddActor(chart_actor_0)
chart_scene_0.SetRenderer(renderer_0)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(1.0, 1.0, 1.0)
renderer_1.SetViewport(0.3, 0.0, 1.0, 0.5)
renderer_1.AddActor(chart_actor_1)
chart_scene_1.SetRenderer(renderer_1)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(1.0, 1.0, 1.0)
renderer_2.SetViewport(0.0, 0.33, 0.5, 0.66)
renderer_2.AddActor(chart_actor_2)
chart_scene_2.SetRenderer(renderer_2)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(1.0, 1.0, 1.0)
renderer_3.SetViewport(0.5, 0.33, 1.0, 0.66)
renderer_3.AddActor(chart_actor_3)
chart_scene_3.SetRenderer(renderer_3)

renderer_4 = vtkRenderer()
renderer_4.SetBackground(1.0, 1.0, 1.0)
renderer_4.SetViewport(0.0, 0.66, 1.0, 1.0)
renderer_4.AddActor(chart_actor_4)
chart_scene_4.SetRenderer(renderer_4)

# Window.
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(800, 900)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.SetWindowName("multiple scalars to colors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
