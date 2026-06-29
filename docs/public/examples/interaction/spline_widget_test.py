#!/usr/bin/env python
# Demonstrate vtkSplineWidget with vtkImagePlaneWidget probing volume data along a spline path.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonComputationalGeometry import vtkKochanekSpline
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkProbeFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkInteractionWidgets import (
    vtkImagePlaneWidget,
    vtkSplineWidget,
)
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingAnnotation import vtkXYPlotActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Source
reader = vtkVolume16Reader()
reader.SetDataDimensions(64, 64)
reader.SetDataByteOrderToLittleEndian()
reader.SetImageRange(1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7FFF)
reader.Update()

# Filters
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

# Mapper + Actor
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(outline_actor)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(1, 1, 1)
renderer_1.SetViewport(0.5, 0, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("spline widget test")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback for image plane widget interaction
def ipw_callback(caller, event_string):
    plane_widget = caller
    if plane_widget.GetPlaneOrientation() == 3:
        spline_widget.SetProjectionPosition(0)
    else:
        spline_widget.SetProjectionPosition(plane_widget.GetSlicePosition())
    spline_widget.GetPolyData(spline_poly)


# Callback for spline widget interaction
def spline_callback(caller, event_string):
    caller.GetPolyData(spline_poly)


# Widgets
# Image plane widget
plane_widget = vtkImagePlaneWidget()
plane_widget.DisplayTextOn()
plane_widget.TextureInterpolateOff()
plane_widget.UserControlledLookupTableOff()
plane_widget.SetInputConnection(reader.GetOutputPort())
plane_widget.KeyPressActivationOn()
plane_widget.SetKeyPressActivationValue("x")
plane_widget.SetResliceInterpolateToNearestNeighbour()
plane_widget.SetInteractor(interactor)
plane_widget.SetPlaneOrientationToXAxes()
plane_widget.SetSliceIndex(32)
plane_widget.GetPlaneProperty().SetColor(1, 0, 0)
plane_widget.AddObserver("InteractionEvent", ipw_callback)
plane_widget.On()
plane_widget.SetInteraction(0)
plane_widget.SetInteraction(1)

# Spline widget
spline_widget = vtkSplineWidget()
spline_widget.SetInteractor(interactor)
spline_widget.SetInputConnection(reader.GetOutputPort())
spline_widget.SetPriority(1.0)
spline_widget.KeyPressActivationOff()
spline_widget.PlaceWidget()
spline_widget.ProjectToPlaneOn()
spline_widget.SetProjectionNormal(0)
spline_widget.SetProjectionPosition(102.4)
spline_widget.SetProjectionNormal(3)
spline_widget.SetPlaneSource(plane_widget.GetPolyDataAlgorithm())

# Use Kochanek splines
x_spline = vtkKochanekSpline()
y_spline = vtkKochanekSpline()
z_spline = vtkKochanekSpline()

parametric_spline = spline_widget.GetParametricSpline()
parametric_spline.SetXSpline(x_spline)
parametric_spline.SetYSpline(y_spline)
parametric_spline.SetZSpline(z_spline)

spline_poly = vtkPolyData()
spline_widget.GetPolyData(spline_poly)

# Probe filter samples the volume along the spline
probe = vtkProbeFilter()
probe.SetInputData(spline_poly)
probe.SetSourceConnection(reader.GetOutputPort())

scalar_range = reader.GetOutput().GetPointData().GetScalars().GetRange()

spline_widget.AddObserver("InteractionEvent", spline_callback)
spline_widget.On()
spline_widget.SetNumberOfHandles(4)
spline_widget.SetNumberOfHandles(5)
spline_widget.SetResolution(399)

# Test On Off mechanism
plane_widget.SetEnabled(0)
spline_widget.EnabledOff()
plane_widget.SetEnabled(1)
spline_widget.EnabledOn()

# Test Set Get handle positions
for i in range(spline_widget.GetNumberOfHandles()):
    pos = spline_widget.GetHandlePosition(i)
    spline_widget.SetHandlePosition(i, pos)

# Test Closed On Off
spline_widget.ClosedOn()
spline_widget.ClosedOff()

# XY plot for profile data
xy_plot = vtkXYPlotActor()
xy_plot.AddDataSetInputConnection(probe.GetOutputPort())
xy_plot.GetPositionCoordinate().SetValue(0.05, 0.05, 0)
xy_plot.GetPosition2Coordinate().SetValue(0.95, 0.95, 0)
xy_plot.SetXValuesToNormalizedArcLength()
xy_plot.SetNumberOfXLabels(6)
xy_plot.SetTitle("Profile Data ")
xy_plot.SetXTitle("s")
xy_plot.SetYTitle("I(s)")
xy_plot.SetXRange(0, 1)
xy_plot.SetYRange(scalar_range[0], scalar_range[1])
xy_plot.GetProperty().SetColor(0, 0, 0)
xy_plot.GetProperty().SetLineWidth(2)
xy_plot.SetLabelFormat("{:g}")
title_prop = xy_plot.GetTitleTextProperty()
title_prop.SetColor(0.02, 0.06, 0.62)
title_prop.SetFontFamilyToArial()
xy_plot.SetAxisTitleTextProperty(title_prop)
xy_plot.SetAxisLabelTextProperty(title_prop)
xy_plot.SetTitleTextProperty(title_prop)

renderer_1.AddViewProp(xy_plot)

# Scene
camera = renderer_0.GetActiveCamera()
camera.Elevation(110)
camera.SetViewUp(0, 0, -1)
camera.Azimuth(45)
camera.SetFocalPoint(100.8, 100.8, 69)
camera.SetPosition(560.949, 560.949, -167.853)
renderer_0.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
