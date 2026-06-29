#!/usr/bin/env python
# Demonstrate vtkInteractorStyleUser with custom mouse bindings on DEM terrain data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter, vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkImagingCore import vtkImageShrink3D
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleUser
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Load DEM data
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

scale = 2
lut = vtkLookupTable()
lut.SetHueRange(0.6, 0)
lut.SetSaturationRange(1.0, 0)
lut.SetValueRange(0.5, 1.0)
elevation_low = scale * dem_reader.GetElevationBounds()[0]
elevation_high = scale * dem_reader.GetElevationBounds()[1]

shrink = vtkImageShrink3D()
shrink.SetShrinkFactors(4, 4, 1)
shrink.SetInputConnection(dem_reader.GetOutputPort())
shrink.AveragingOn()

geometry_filter = vtkImageDataGeometryFilter()
geometry_filter.SetInputConnection(shrink.GetOutputPort())
geometry_filter.ReleaseDataFlagOn()

warp = vtkWarpScalar()
warp.SetInputConnection(geometry_filter.GetOutputPort())
warp.SetNormal(0, 0, 1)
warp.UseNormalOn()
warp.SetScaleFactor(scale)
warp.ReleaseDataFlagOn()

elevation = vtkElevationFilter()
elevation.SetInputConnection(warp.GetOutputPort())
elevation.SetLowPoint(0, 0, elevation_low)
elevation.SetHighPoint(0, 0, elevation_high)
elevation.SetScalarRange(elevation_low, elevation_high)
elevation.ReleaseDataFlagOn()

normals = vtkPolyDataNormals()
normals.SetInputConnection(elevation.GetOutputPort())
normals.SetFeatureAngle(60)
normals.ConsistencyOff()
normals.SplittingOff()
normals.ReleaseDataFlagOn()
normals.Update()

dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(normals.GetOutputPort())
dem_mapper.SetScalarRange(elevation_low, elevation_high)
dem_mapper.SetLookupTable(lut)

dem_actor = vtkActor()
dem_actor.SetMapper(dem_mapper)

# Rendering
renderer = vtkRenderer()
renderer.AddActor(dem_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("style user")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.LightFollowCameraOff()

camera = renderer.GetActiveCamera()
camera.SetViewUp(0, 0, 1)
camera.SetFocalPoint(dem_reader.GetOutput().GetCenter())
camera.SetPosition(1, 0, 0)
renderer.ResetCamera()
camera.Elevation(25)
camera.Azimuth(125)
camera.Zoom(1.25)

# Set up vtkInteractorStyleUser with custom callbacks
style = vtkInteractorStyleUser()
interactor.SetInteractorStyle(style)

# Mouse state
left = 0
middle = 0
right = 0
old_pick_w = [0, 0, 0, 0]
new_pick_w = [0, 0, 0, 0]
fp_d = [0, 0, 0]
motion_d = [0, 0]
motion_w = [0, 0, 0]
camera_ref = None
fp_w = None
pos_w = None

def get_motion():
    global old_pick_w, new_pick_w, fp_d, motion_d, motion_w, camera_ref, fp_w, pos_w
    current_style = interactor.GetInteractorStyle()
    old_pick_d = interactor.GetLastEventPosition()
    new_pick_d = interactor.GetEventPosition()
    motion_d[0] = new_pick_d[0] - old_pick_d[0]
    motion_d[1] = new_pick_d[1] - old_pick_d[1]
    camera_ref = renderer.GetActiveCamera()
    fp_w = camera_ref.GetFocalPoint()
    pos_w = camera_ref.GetPosition()
    current_style.ComputeWorldToDisplay(renderer, fp_w[0], fp_w[1], fp_w[2], fp_d)
    focal_depth = fp_d[2]
    current_style.ComputeDisplayToWorld(renderer, old_pick_d[0], old_pick_d[1], focal_depth, old_pick_w)
    current_style.ComputeDisplayToWorld(renderer, new_pick_d[0], new_pick_d[1], focal_depth, new_pick_w)
    motion_w[0] = old_pick_w[0] - new_pick_w[0]
    motion_w[1] = old_pick_w[1] - new_pick_w[1]
    motion_w[2] = old_pick_w[2] - new_pick_w[2]

def left_down(widget, event_string):
    global left
    left = 1

def left_up(widget, event_string):
    global left
    left = 0

def middle_down(widget, event_string):
    global middle
    middle = 1

def middle_up(widget, event_string):
    global middle
    middle = 0

def right_down(widget, event_string):
    global right
    right = 1

def right_up(widget, event_string):
    global right
    right = 0

def wheel_forward(widget, event_string):
    renderer.GetActiveCamera().Zoom(1.1)
    interactor.Render()

def wheel_backward(widget, event_string):
    renderer.GetActiveCamera().Zoom(0.9)
    interactor.Render()

def mouse_move(widget, event_string):
    global left, middle, right
    if left == 1:
        get_motion()
        camera_ref.SetFocalPoint(fp_w[0] + motion_w[0], fp_w[1] + motion_w[1], fp_w[2] + motion_w[2])
        camera_ref.SetPosition(pos_w[0] + motion_w[0], pos_w[1] + motion_w[1], pos_w[2] + motion_w[2])
        interactor.Render()
    if middle == 1:
        get_motion()
        if abs(motion_d[0]) > abs(motion_d[1]):
            camera_ref.Azimuth(-2.0 * motion_d[0])
        else:
            camera_ref.Elevation(-motion_d[1])
        interactor.Render()
    if right == 1:
        get_motion()
        if abs(motion_d[0]) > abs(motion_d[1]):
            camera_ref.Azimuth(-2.0 * motion_d[0])
        else:
            camera_ref.Zoom(1 + motion_d[1] / 100.0)
        interactor.Render()

style.AddObserver("LeftButtonPressEvent", left_down)
style.AddObserver("LeftButtonReleaseEvent", left_up)
style.AddObserver("MiddleButtonPressEvent", middle_down)
style.AddObserver("MiddleButtonReleaseEvent", middle_up)
style.AddObserver("RightButtonPressEvent", right_down)
style.AddObserver("RightButtonReleaseEvent", right_up)
style.AddObserver("MouseWheelForwardEvent", wheel_forward)
style.AddObserver("MouseWheelBackwardEvent", wheel_backward)
style.AddObserver("MouseMoveEvent", mouse_move)

interactor.Initialize()
interactor.Start()
