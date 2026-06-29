#!/usr/bin/env python
# Demonstrate vtkResliceCursorWidget with thick line representation in a four-pane layout.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkInteractionWidgets import (
    vtkImagePlaneWidget,
    vtkResliceCursor,
    vtkResliceCursorThickLineRepresentation,
    vtkResliceCursorWidget,
)
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Load headsq/quarter volume data.
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
file_prefix = os.path.join(data_dir, "headsq", "quarter")

reader = vtkVolume16Reader()
reader.SetDataDimensions(64, 64)
reader.SetDataByteOrderToLittleEndian()
reader.SetImageRange(1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetFilePrefix(file_prefix)
reader.SetDataMask(0x7FFF)
reader.Update()

# Outline of the volume.
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderers
renderer_x = vtkRenderer()
renderer_x.SetBackground(0.3, 0.1, 0.1)
renderer_x.SetViewport(0, 0, 0.5, 0.5)

renderer_y = vtkRenderer()
renderer_y.SetBackground(0.1, 0.3, 0.1)
renderer_y.SetViewport(0.5, 0, 1, 0.5)

renderer_z = vtkRenderer()
renderer_z.SetBackground(0.1, 0.1, 0.3)
renderer_z.SetViewport(0, 0.5, 0.5, 1)

renderer_3d = vtkRenderer()
renderer_3d.AddActor(outline_actor)
renderer_3d.SetBackground(0.1, 0.1, 0.1)
renderer_3d.SetViewport(0.5, 0.5, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_x)
render_window.AddRenderer(renderer_y)
render_window.AddRenderer(renderer_z)
render_window.AddRenderer(renderer_3d)
render_window.SetWindowName("reslice cursor thick four pane")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Cell picker for the image plane widgets.
picker = vtkCellPicker()
picker.SetTolerance(0.005)

ipw_prop = vtkProperty()

# Image plane widgets (X, Y, Z).
image_dims = reader.GetOutput().GetDimensions()

plane_widget_x = vtkImagePlaneWidget()
plane_widget_x.SetInteractor(interactor)
plane_widget_x.SetPicker(picker)
plane_widget_x.RestrictPlaneToVolumeOn()
plane_widget_x.GetPlaneProperty().SetColor(1, 0, 0)
plane_widget_x.SetTexturePlaneProperty(ipw_prop)
plane_widget_x.TextureInterpolateOff()
plane_widget_x.SetResliceInterpolateToLinear()
plane_widget_x.SetInputConnection(reader.GetOutputPort())
plane_widget_x.SetPlaneOrientation(0)
plane_widget_x.SetSliceIndex(image_dims[0] // 2)
plane_widget_x.DisplayTextOn()
plane_widget_x.SetDefaultRenderer(renderer_3d)
plane_widget_x.SetWindowLevel(1358, -27)
plane_widget_x.On()
plane_widget_x.InteractionOn()

plane_widget_y = vtkImagePlaneWidget()
plane_widget_y.SetInteractor(interactor)
plane_widget_y.SetPicker(picker)
plane_widget_y.RestrictPlaneToVolumeOn()
plane_widget_y.GetPlaneProperty().SetColor(0, 1, 0)
plane_widget_y.SetTexturePlaneProperty(ipw_prop)
plane_widget_y.TextureInterpolateOff()
plane_widget_y.SetResliceInterpolateToLinear()
plane_widget_y.SetInputConnection(reader.GetOutputPort())
plane_widget_y.SetPlaneOrientation(1)
plane_widget_y.SetSliceIndex(image_dims[1] // 2)
plane_widget_y.DisplayTextOn()
plane_widget_y.SetDefaultRenderer(renderer_3d)
plane_widget_y.SetWindowLevel(1358, -27)
plane_widget_y.On()
plane_widget_y.InteractionOn()

plane_widget_z = vtkImagePlaneWidget()
plane_widget_z.SetInteractor(interactor)
plane_widget_z.SetPicker(picker)
plane_widget_z.RestrictPlaneToVolumeOn()
plane_widget_z.GetPlaneProperty().SetColor(0, 0, 1)
plane_widget_z.SetTexturePlaneProperty(ipw_prop)
plane_widget_z.TextureInterpolateOff()
plane_widget_z.SetResliceInterpolateToLinear()
plane_widget_z.SetInputConnection(reader.GetOutputPort())
plane_widget_z.SetPlaneOrientation(2)
plane_widget_z.SetSliceIndex(image_dims[2] // 2)
plane_widget_z.DisplayTextOn()
plane_widget_z.SetDefaultRenderer(renderer_3d)
plane_widget_z.SetWindowLevel(1358, -27)
plane_widget_z.On()
plane_widget_z.InteractionOn()

plane_widget_y.SetLookupTable(plane_widget_x.GetLookupTable())
plane_widget_z.SetLookupTable(plane_widget_x.GetLookupTable())

plane_widgets = [plane_widget_x, plane_widget_y, plane_widget_z]

# Reslice cursor with thick mode enabled.
reslice_cursor = vtkResliceCursor()
reslice_cursor.SetCenter(reader.GetOutput().GetCenter())
reslice_cursor.SetThickMode(1)
reslice_cursor.SetThickness(10, 10, 10)
reslice_cursor.SetImage(reader.GetOutput())

scalar_range = reader.GetOutput().GetScalarRange()
min_val = scalar_range[0]
window_level_width = scalar_range[1] - scalar_range[0]
window_level_center = (scalar_range[0] + scalar_range[1]) / 2.0

# Reslice cursor widget X
reslice_widget_x = vtkResliceCursorWidget()
reslice_widget_x.SetInteractor(interactor)

reslice_rep_x = vtkResliceCursorThickLineRepresentation()
reslice_widget_x.SetRepresentation(reslice_rep_x)
reslice_rep_x.GetResliceCursorActor().GetCursorAlgorithm().SetResliceCursor(reslice_cursor)
reslice_rep_x.GetResliceCursorActor().GetCursorAlgorithm().SetReslicePlaneNormal(0)

reslice_x = reslice_rep_x.GetReslice()
if reslice_x and reslice_x.IsA("vtkImageReslice"):
    reslice_x.SetBackgroundColor(min_val, min_val, min_val, min_val)

reslice_widget_x.SetDefaultRenderer(renderer_x)
reslice_widget_x.SetEnabled(1)

renderer_x.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_x.GetActiveCamera().SetPosition(1, 0, 0)
renderer_x.GetActiveCamera().ParallelProjectionOn()
renderer_x.GetActiveCamera().SetViewUp(0, 0, -1)
renderer_x.ResetCamera()

reslice_rep_x.SetWindowLevel(window_level_width, window_level_center)
plane_widget_x.SetWindowLevel(window_level_width, window_level_center)

plane_widget_x.GetColorMap().SetLookupTable(reslice_rep_x.GetLookupTable())

reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(0).SetRepresentationToWireframe()
reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(0).RenderLinesAsTubesOn()
reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(0).SetLineWidth(2)
reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(1).SetRepresentationToWireframe()
reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(1).RenderLinesAsTubesOn()
reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(1).SetLineWidth(2)
reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(2).SetRepresentationToWireframe()
reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(2).RenderLinesAsTubesOn()
reslice_rep_x.GetResliceCursorActor().GetCenterlineProperty(2).SetLineWidth(2)
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(0).SetRepresentationToWireframe()
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(0).RenderLinesAsTubesOn()
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(0).SetLineWidth(2)
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(1).SetRepresentationToWireframe()
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(1).RenderLinesAsTubesOn()
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(1).SetLineWidth(2)
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(2).SetRepresentationToWireframe()
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(2).RenderLinesAsTubesOn()
reslice_rep_x.GetResliceCursorActor().GetThickSlabProperty(2).SetLineWidth(2)

# Reslice cursor widget Y
reslice_widget_y = vtkResliceCursorWidget()
reslice_widget_y.SetInteractor(interactor)

reslice_rep_y = vtkResliceCursorThickLineRepresentation()
reslice_widget_y.SetRepresentation(reslice_rep_y)
reslice_rep_y.GetResliceCursorActor().GetCursorAlgorithm().SetResliceCursor(reslice_cursor)
reslice_rep_y.GetResliceCursorActor().GetCursorAlgorithm().SetReslicePlaneNormal(1)

reslice_y = reslice_rep_y.GetReslice()
if reslice_y and reslice_y.IsA("vtkImageReslice"):
    reslice_y.SetBackgroundColor(min_val, min_val, min_val, min_val)

reslice_widget_y.SetDefaultRenderer(renderer_y)
reslice_widget_y.SetEnabled(1)

renderer_y.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_y.GetActiveCamera().SetPosition(0, 1, 0)
renderer_y.GetActiveCamera().ParallelProjectionOn()
renderer_y.GetActiveCamera().SetViewUp(0, 0, 1)
renderer_y.ResetCamera()

reslice_rep_y.SetWindowLevel(window_level_width, window_level_center)
plane_widget_y.SetWindowLevel(window_level_width, window_level_center)

reslice_rep_y.SetLookupTable(reslice_rep_x.GetLookupTable())
plane_widget_y.GetColorMap().SetLookupTable(reslice_rep_x.GetLookupTable())

reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(0).SetRepresentationToWireframe()
reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(0).RenderLinesAsTubesOn()
reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(0).SetLineWidth(2)
reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(1).SetRepresentationToWireframe()
reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(1).RenderLinesAsTubesOn()
reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(1).SetLineWidth(2)
reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(2).SetRepresentationToWireframe()
reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(2).RenderLinesAsTubesOn()
reslice_rep_y.GetResliceCursorActor().GetCenterlineProperty(2).SetLineWidth(2)
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(0).SetRepresentationToWireframe()
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(0).RenderLinesAsTubesOn()
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(0).SetLineWidth(2)
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(1).SetRepresentationToWireframe()
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(1).RenderLinesAsTubesOn()
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(1).SetLineWidth(2)
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(2).SetRepresentationToWireframe()
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(2).RenderLinesAsTubesOn()
reslice_rep_y.GetResliceCursorActor().GetThickSlabProperty(2).SetLineWidth(2)

# Reslice cursor widget Z
reslice_widget_z = vtkResliceCursorWidget()
reslice_widget_z.SetInteractor(interactor)

reslice_rep_z = vtkResliceCursorThickLineRepresentation()
reslice_widget_z.SetRepresentation(reslice_rep_z)
reslice_rep_z.GetResliceCursorActor().GetCursorAlgorithm().SetResliceCursor(reslice_cursor)
reslice_rep_z.GetResliceCursorActor().GetCursorAlgorithm().SetReslicePlaneNormal(2)

reslice_z = reslice_rep_z.GetReslice()
if reslice_z and reslice_z.IsA("vtkImageReslice"):
    reslice_z.SetBackgroundColor(min_val, min_val, min_val, min_val)

reslice_widget_z.SetDefaultRenderer(renderer_z)
reslice_widget_z.SetEnabled(1)

renderer_z.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_z.GetActiveCamera().SetPosition(0, 0, 1)
renderer_z.GetActiveCamera().ParallelProjectionOn()
renderer_z.GetActiveCamera().SetViewUp(0, 1, 0)
renderer_z.ResetCamera()

reslice_rep_z.SetWindowLevel(window_level_width, window_level_center)
plane_widget_z.SetWindowLevel(window_level_width, window_level_center)

reslice_rep_z.SetLookupTable(reslice_rep_x.GetLookupTable())
plane_widget_z.GetColorMap().SetLookupTable(reslice_rep_x.GetLookupTable())

reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(0).SetRepresentationToWireframe()
reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(0).RenderLinesAsTubesOn()
reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(0).SetLineWidth(2)
reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(1).SetRepresentationToWireframe()
reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(1).RenderLinesAsTubesOn()
reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(1).SetLineWidth(2)
reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(2).SetRepresentationToWireframe()
reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(2).RenderLinesAsTubesOn()
reslice_rep_z.GetResliceCursorActor().GetCenterlineProperty(2).SetLineWidth(2)
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(0).SetRepresentationToWireframe()
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(0).RenderLinesAsTubesOn()
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(0).SetLineWidth(2)
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(1).SetRepresentationToWireframe()
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(1).RenderLinesAsTubesOn()
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(1).SetLineWidth(2)
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(2).SetRepresentationToWireframe()
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(2).RenderLinesAsTubesOn()
reslice_rep_z.GetResliceCursorActor().GetThickSlabProperty(2).SetLineWidth(2)

reslice_cursor_widgets = [reslice_widget_x, reslice_widget_y, reslice_widget_z]


# Callback to tie reslice cursor and image plane widgets together.
def reslice_callback(caller, event):
    ipw = None
    for i in range(3):
        if caller is plane_widgets[i]:
            ipw = caller
            break

    if ipw is not None:
        wl = ipw.GetWindowLevel()
        for i in range(3):
            if plane_widgets[i] is not ipw:
                plane_widgets[i].SetWindowLevel(wl[0], wl[1], 1)

    rcw_caller = None
    for i in range(3):
        if caller is reslice_cursor_widgets[i]:
            rcw_caller = caller
            break

    if rcw_caller is not None:
        callback_rep = rcw_caller.GetRepresentation()
        rc = callback_rep.GetResliceCursorActor().GetCursorAlgorithm().GetResliceCursor()
        for i in range(3):
            ps = plane_widgets[i].GetPolyDataAlgorithm()
            ps.SetNormal(rc.GetPlane(i).GetNormal())
            ps.SetCenter(rc.GetPlane(i).GetOrigin())
            plane_widgets[i].UpdatePlacement()

    reslice_widget_x.Render()


reslice_widget_x.AddObserver(
    vtkResliceCursorWidget.ResliceAxesChangedEvent, reslice_callback
)
reslice_widget_y.AddObserver(
    vtkResliceCursorWidget.ResliceAxesChangedEvent, reslice_callback
)
reslice_widget_z.AddObserver(
    vtkResliceCursorWidget.ResliceAxesChangedEvent, reslice_callback
)

# Scene
render_window.Render()

renderer_3d.GetActiveCamera().Elevation(110)
renderer_3d.GetActiveCamera().SetViewUp(0, 0, -1)
renderer_3d.GetActiveCamera().Azimuth(45)
renderer_3d.GetActiveCamera().Dolly(1.15)
renderer_3d.ResetCameraClippingRange()

style = vtkInteractorStyleImage()
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
