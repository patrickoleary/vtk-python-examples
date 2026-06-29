#!/usr/bin/env python

# Demonstrate vtkXYPlotActor with three line probes through PLOT3D data.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
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
probe.Update()

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
probe_2.Update()

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
probe_3.Update()

# Tube filter for visualization
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

# XY Plot 1 — pressure vs arc length (zoomed)
xyplot = vtkXYPlotActor()
xyplot.AddDataSetInput(probe.GetOutput())
xyplot.AddDataSetInputConnection(probe_2.GetOutputPort())
xyplot.AddDataSetInput(probe_3.GetOutput())
xyplot.GetPositionCoordinate().SetValue(0.0, 0.67, 0)
xyplot.GetPosition2Coordinate().SetValue(1.0, 0.33, 0)
xyplot.SetXValuesToArcLength()
xyplot.SetNumberOfXLabels(6)
xyplot.SetTitle("Pressure vs. Arc Length (Zoomed View)")
xyplot.SetXTitle("")
xyplot.SetYTitle("P")
xyplot.SetXRange(0.1, 0.35)
xyplot.SetYRange(0.2, 0.4)
xyplot.GetProperty().SetColor(0, 0, 0)
xyplot.GetProperty().SetLineWidth(2)
tprop = xyplot.GetTitleTextProperty()
tprop.SetColor(xyplot.GetProperty().GetColor())
xyplot.SetAxisTitleTextProperty(tprop)
xyplot.SetAxisLabelTextProperty(tprop)
xyplot.SetLabelFormat("%-#6.2f")

# XY Plot 2 — pressure vs normalized arc length
xyplot_2 = vtkXYPlotActor()
xyplot_2.AddDataSetInput(probe.GetOutput())
xyplot_2.AddDataSetInputConnection(probe_2.GetOutputPort())
xyplot_2.AddDataSetInputConnection(probe_3.GetOutputPort())
xyplot_2.GetPositionCoordinate().SetValue(0.00, 0.33, 0)
xyplot_2.GetPosition2Coordinate().SetValue(1.0, 0.33, 0)
xyplot_2.SetXValuesToNormalizedArcLength()
xyplot_2.SetNumberOfXLabels(6)
xyplot_2.SetTitle("Pressure vs. Normalized Arc Length")
xyplot_2.SetXTitle("")
xyplot_2.SetYTitle("P")
xyplot_2.PlotPointsOn()
xyplot_2.PlotLinesOff()
xyplot_2.GetProperty().SetColor(1, 0, 0)
xyplot_2.GetProperty().SetPointSize(2)
tprop_2 = xyplot_2.GetTitleTextProperty()
tprop_2.SetColor(xyplot_2.GetProperty().GetColor())
xyplot_2.SetAxisTitleTextProperty(tprop_2)
xyplot_2.SetAxisLabelTextProperty(tprop_2)
xyplot_2.SetLabelFormat(xyplot.GetLabelFormat())

# XY Plot 3 — pressure vs point id
xyplot_3 = vtkXYPlotActor()
xyplot_3.AddDataSetInputConnection(probe.GetOutputPort())
xyplot_3.AddDataSetInputConnection(probe_2.GetOutputPort())
xyplot_3.AddDataSetInputConnection(probe_3.GetOutputPort())
xyplot_3.GetPositionCoordinate().SetValue(0.0, 0.0, 0)
xyplot_3.GetPosition2Coordinate().SetValue(1.0, 0.33, 0)
xyplot_3.SetXValuesToIndex()
xyplot_3.SetNumberOfXLabels(6)
xyplot_3.SetTitle("Pressure vs. Point Id")
xyplot_3.SetXTitle("Probe Length")
xyplot_3.SetYTitle("P")
xyplot_3.PlotPointsOn()
xyplot_3.GetProperty().SetColor(0, 0, 1)
xyplot_3.GetProperty().SetPointSize(3)
tprop_3 = xyplot_3.GetTitleTextProperty()
tprop_3.SetColor(xyplot_3.GetProperty().GetColor())
xyplot_3.SetAxisTitleTextProperty(tprop_3)
xyplot_3.SetAxisLabelTextProperty(tprop_3)
xyplot_3.SetLabelFormat(xyplot.GetLabelFormat())

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
renderer_1.AddViewProp(xyplot_2)
renderer_1.AddViewProp(xyplot_3)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("xy plot")
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
