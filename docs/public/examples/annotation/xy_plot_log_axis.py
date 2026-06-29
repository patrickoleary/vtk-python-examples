#!/usr/bin/env python

# Demonstrate vtkXYPlotActor with log-x axis and data object momentum plots.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkDataSetToDataObjectFilter,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkGlyphSource2D, vtkLineSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingAnnotation import vtkXYPlotActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data path
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PLOT3D data
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()
output = pl3d.GetOutput().GetBlock(0)

# Line source
line = vtkLineSource()
line.SetResolution(30)

# Probe 1
trans_l1 = vtkTransform()
trans_l1.Translate(3.7, 0.0, 28.37)
trans_l1.Scale(5, 5, 5)
trans_l1.RotateY(90)

tf = vtkTransformPolyDataFilter()
tf.SetInputConnection(line.GetOutputPort())
tf.SetTransform(trans_l1)

probe = vtkProbeFilter()
probe.SetInputConnection(tf.GetOutputPort())
probe.SetSourceData(output)

# Probe 2
trans_l2 = vtkTransform()
trans_l2.Translate(9.2, 0.0, 31.20)
trans_l2.Scale(5, 5, 5)
trans_l2.RotateY(90)

tf_2 = vtkTransformPolyDataFilter()
tf_2.SetInputConnection(line.GetOutputPort())
tf_2.SetTransform(trans_l2)

probe_2 = vtkProbeFilter()
probe_2.SetInputConnection(tf_2.GetOutputPort())
probe_2.SetSourceData(output)

# Probe 3
trans_l3 = vtkTransform()
trans_l3.Translate(13.27, 0.0, 33.40)
trans_l3.Scale(4.5, 4.5, 4.5)
trans_l3.RotateY(90)

tf_3 = vtkTransformPolyDataFilter()
tf_3.SetInputConnection(line.GetOutputPort())
tf_3.SetTransform(trans_l3)

probe_3 = vtkProbeFilter()
probe_3.SetInputConnection(tf_3.GetOutputPort())
probe_3.SetSourceData(output)

# Tube for line visualization
append_f = vtkAppendPolyData()
append_f.AddInputData(probe.GetPolyDataOutput())
append_f.AddInputData(probe_2.GetPolyDataOutput())
append_f.AddInputData(probe_3.GetPolyDataOutput())

tuber = vtkTubeFilter()
tuber.SetInputConnection(append_f.GetOutputPort())
tuber.SetRadius(0.1)

line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(tuber.GetOutputPort())

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)

# Glyph sources
triangle = vtkGlyphSource2D()
triangle.SetGlyphTypeToTriangle()
triangle.Update()

cross = vtkGlyphSource2D()
cross.SetGlyphTypeToCross()
cross.Update()

# XY Plot 1 — pressure vs log10 Z-value
xyplot = vtkXYPlotActor()
xyplot.AddDataSetInputConnection(probe.GetOutputPort())
xyplot.AddDataSetInputConnection(probe_2.GetOutputPort())
xyplot.AddDataSetInputConnection(probe_3.GetOutputPort())
xyplot.GetPositionCoordinate().SetValue(0.0, 0.5, 0)
xyplot.GetPosition2Coordinate().SetValue(1.0, 0.5, 0)
xyplot.SetXValuesToValue()
xyplot.SetPointComponent(0, 2)
xyplot.SetPointComponent(1, 2)
xyplot.SetPointComponent(2, 2)
xyplot.LogxOn()
xyplot.SetNumberOfXLabels(6)
xyplot.SetTitle("Pressure vs. Log10 Probe Z-Value")
xyplot.SetXTitle("")
xyplot.SetYTitle("P")
xyplot.PlotCurveLinesOn()
xyplot.PlotCurvePointsOn()
xyplot.SetPlotLines(0, 1)
xyplot.SetPlotLines(1, 0)
xyplot.SetPlotLines(2, 1)
xyplot.SetPlotPoints(0, 0)
xyplot.SetPlotPoints(1, 1)
xyplot.SetPlotPoints(2, 1)
xyplot.GetProperty().SetColor(0, 0, 0)
xyplot.GetProperty().SetLineWidth(1)
xyplot.GetProperty().SetPointSize(3)
xyplot.SetPlotSymbol(2, triangle.GetOutput())
xyplot.SetPlotColor(2, 0, 0, 1)
xyplot.SetGlyphSize(0.025)
tprop = xyplot.GetTitleTextProperty()
tprop.SetColor(xyplot.GetProperty().GetColor())
xyplot.SetAxisTitleTextProperty(tprop)
xyplot.SetAxisLabelTextProperty(tprop)
xyplot.SetLabelFormat("%-#6.2f")

# Data object filters for momentum
ds2do = vtkDataSetToDataObjectFilter()
ds2do.SetInputConnection(probe.GetOutputPort())
ds2do.ModernTopologyOff()
ds2do.Update()

ds2do_2 = vtkDataSetToDataObjectFilter()
ds2do_2.SetInputConnection(probe.GetOutputPort())
ds2do_2.ModernTopologyOff()

ds2do_3 = vtkDataSetToDataObjectFilter()
ds2do_3.SetInputConnection(probe.GetOutputPort())
ds2do_3.ModernTopologyOff()
ds2do_3.Update()

# XY Plot 3 — momentum vs log10 Z-value
xyplot_3 = vtkXYPlotActor()
xyplot_3.AddDataObjectInput(ds2do.GetOutput())
xyplot_3.SetDataObjectXComponent(0, 2)
xyplot_3.SetDataObjectYComponent(0, 5)
xyplot_3.SetPlotColor(0, 1, 0, 0)
xyplot_3.SetPlotLabel(0, "Mx")
xyplot_3.AddDataObjectInputConnection(ds2do_2.GetOutputPort())
xyplot_3.SetDataObjectXComponent(1, 2)
xyplot_3.SetDataObjectYComponent(1, 6)
xyplot_3.SetPlotColor(1, 0, 1, 0)
xyplot_3.SetPlotLabel(1, "My")
xyplot_3.AddDataObjectInput(ds2do_3.GetOutput())
xyplot_3.SetDataObjectXComponent(2, 2)
xyplot_3.SetDataObjectYComponent(2, 7)
xyplot_3.SetPlotColor(2, 0, 0, 1)
xyplot_3.SetPlotLabel(2, "Mz")
xyplot_3.GetPositionCoordinate().SetValue(0.0, 0.0, 0)
xyplot_3.GetPosition2Coordinate().SetValue(1.0, 0.5, 0)
xyplot_3.SetXValuesToValue()
xyplot_3.SetNumberOfXLabels(6)
xyplot_3.SetTitle("Momentum Component vs. Log10 Probe Z-Value")
xyplot_3.SetXTitle("Log10 Probe Z-Value")
xyplot_3.SetYTitle("M")
xyplot_3.GetProperty().SetColor(0, 0, 1)
xyplot_3.GetProperty().SetPointSize(5)
xyplot_3.PlotCurveLinesOn()
xyplot_3.PlotCurvePointsOn()
xyplot_3.SetPlotLines(0, 1)
xyplot_3.SetPlotLines(1, 0)
xyplot_3.SetPlotLines(2, 1)
xyplot_3.SetPlotPoints(0, 0)
xyplot_3.SetPlotPoints(1, 1)
xyplot_3.SetPlotPoints(2, 1)
xyplot_3.LogxOn()
tprop_3 = xyplot_3.GetTitleTextProperty()
tprop_3.SetColor(xyplot_3.GetProperty().GetColor())
xyplot_3.SetAxisTitleTextProperty(tprop_3)
xyplot_3.SetAxisLabelTextProperty(tprop_3)
xyplot_3.GetYAxisActor2D().SetLabelFormat("%4.0f")
xyplot_3.GetXAxisActor2D().SetLabelFormat("%-#6.2f")

# Outline
sg_outline = vtkStructuredGridOutlineFilter()
sg_outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(sg_outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer 0 — 3D view
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.6784, 0.8471, 0.9020)
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(line_actor)

# Renderer 1 — plots
renderer_1 = vtkRenderer()
renderer_1.SetBackground(1, 1, 1)
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.AddViewProp(xyplot)
renderer_1.AddViewProp(xyplot_3)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("xy plot log axis")
render_window.SetMultiSamples(0)
render_window.SetSize(790, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam_1 = renderer_0.GetActiveCamera()
cam_1.SetClippingRange(3.95297, 100)
cam_1.SetFocalPoint(8.88908, 0.595038, 29.3342)
cam_1.SetPosition(-12.3332, 31.7479, 41.2387)
cam_1.SetViewUp(0.060772, -0.319905, 0.945498)

interactor.Initialize()
interactor.Start()
