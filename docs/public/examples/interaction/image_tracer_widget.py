#!/usr/bin/env python
# Demonstrate vtkImageTracerWidget with vtkSplineWidget on a medical image slice.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkCommand, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkExtractVOI, vtkImageShiftScale
from vtkmodules.vtkImagingStencil import vtkImageStencil, vtkPolyDataToImageStencil
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkInteractionWidgets import vtkImageTracerWidget, vtkSplineWidget
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Tracer widget needs the line to be at the correct z, so shift polys back.
vtkMapper.SetResolveCoincidentTopologyToPolygonOffset()
vtkMapper.SetResolveCoincidentTopologyPolygonOffsetParameters(0, 2)
vtkMapper.SetResolveCoincidentTopologyLineOffsetParameters(0, 0)

# Dataset
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.SetDataByteOrderToLittleEndian()
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)
volume_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
volume_reader.ReleaseDataFlagOn()
volume_reader.SetDataMask(0x7FFF)
volume_reader.Update()

# Filter: shift and scale to unsigned char for display
scalar_range = volume_reader.GetOutput().GetScalarRange()
shifter = vtkImageShiftScale()
shifter.SetShift(-1.0 * scalar_range[0])
shifter.SetScale(255.0 / (scalar_range[1] - scalar_range[0]))
shifter.SetOutputScalarTypeToUnsignedChar()
shifter.SetInputConnection(volume_reader.GetOutputPort())
shifter.ReleaseDataFlagOff()
shifter.Update()

# Actor 0: y-z plane in left renderer
image_actor_0 = vtkImageActor()
image_actor_0.GetMapper().SetInputConnection(shifter.GetOutputPort())
image_actor_0.VisibilityOn()
image_actor_0.SetDisplayExtent(31, 31, 0, 63, 0, 92)
image_actor_0.InterpolateOff()

# Filter: extract VOI for right renderer
extract = vtkExtractVOI()
extract.SetVOI(image_actor_0.GetDisplayExtent())
extract.SetSampleRate(1, 1, 1)
extract.SetInputConnection(shifter.GetOutputPort())
extract.ReleaseDataFlagOff()
extract.Update()

# Actor 1: extracted VOI in right renderer
image_actor_1 = vtkImageActor()
image_actor_1.GetMapper().SetInputConnection(extract.GetOutputPort())
image_actor_1.VisibilityOn()
image_actor_1.SetDisplayExtent(extract.GetVOI())
image_actor_1.InterpolateOff()

# Stencil pipeline for 2D region of interest extraction
path_poly = vtkPolyData()
spline_points = vtkPoints()
spline_poly = vtkPolyData()

extrude = vtkLinearExtrusionFilter()
extrude.SetInputData(spline_poly)
extrude.SetScaleFactor(1)
extrude.SetExtrusionTypeToNormalExtrusion()
extrude.SetVector(1, 0, 0)

stencil_transform = vtkTransform()
stencil_transform.Translate(-0.5, 0, 0)

poly_filter = vtkTransformPolyDataFilter()
poly_filter.SetInputConnection(extrude.GetOutputPort())
poly_filter.SetTransform(stencil_transform)

data_to_stencil = vtkPolyDataToImageStencil()
data_to_stencil.SetInputConnection(poly_filter.GetOutputPort())
data_to_stencil.SetInformationInput(extract.GetOutput())

stencil = vtkImageStencil()
stencil.SetInputConnection(extract.GetOutputPort())
stencil.SetStencilConnection(data_to_stencil.GetOutputPort())
stencil.ReverseStencilOff()
stencil.SetBackgroundValue(128)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0.4, 0.4, 0.5)
renderer_0.AddViewProp(image_actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0.5, 0.4, 0.4)
renderer_1.AddViewProp(image_actor_1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("image tracer widget")
render_window.SetSize(480, 240)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)
interactor.SetRenderWindow(render_window)


# Callbacks
def tracer_callback(caller, event):
    closed = image_tracer_widget.IsClosed()
    spline_widget.SetClosed(closed)

    if not closed:
        image_actor_1.GetMapper().SetInputConnection(extract.GetOutputPort())

    npts = image_tracer_widget.GetNumberOfHandles()
    if npts < 2:
        return

    image_tracer_widget.GetPath(path_poly)
    pts = path_poly.GetPoints()
    if not pts:
        return

    spline_widget.InitializeHandles(pts)

    if closed:
        spline_widget.GetPolyData(spline_poly)
        stencil.Update()
        image_actor_1.GetMapper().SetInputConnection(stencil.GetOutputPort())


def spline_callback(caller, event):
    npts = spline_widget.GetNumberOfHandles()
    closed = spline_widget.IsClosed()

    spline_points.Reset()
    for i in range(npts):
        spline_points.InsertNextPoint(spline_widget.GetHandlePosition(i))

    if closed:
        if image_tracer_widget.GetAutoClose():
            spline_points.InsertNextPoint(spline_widget.GetHandlePosition(0))
        spline_widget.GetPolyData(spline_poly)
        stencil.Update()
        image_actor_1.GetMapper().SetInputConnection(stencil.GetOutputPort())

    image_tracer_widget.InitializeHandles(spline_points)


# Widget: image tracer in left renderer
image_tracer_widget = vtkImageTracerWidget()
image_tracer_widget.SetDefaultRenderer(renderer_0)
image_tracer_widget.SetCaptureRadius(1.5)
image_tracer_widget.GetGlyphSource().SetColor(1, 0, 0)
image_tracer_widget.GetGlyphSource().SetScale(9.0)
image_tracer_widget.GetGlyphSource().SetRotationAngle(45.0)
image_tracer_widget.GetGlyphSource().Modified()
image_tracer_widget.ProjectToPlaneOn()
image_tracer_widget.SetProjectionNormalToXAxes()
image_tracer_widget.SetProjectionPosition(image_actor_0.GetBounds()[0])
image_tracer_widget.SetViewProp(image_actor_0)
image_tracer_widget.SetInputConnection(shifter.GetOutputPort())
image_tracer_widget.SetInteractor(interactor)
image_tracer_widget.PlaceWidget()
image_tracer_widget.SnapToImageOff()
image_tracer_widget.AutoCloseOn()
image_tracer_widget.AddObserver(vtkCommand.EndInteractionEvent, tracer_callback)
image_tracer_widget.On()

# Widget: spline in right renderer
spline_widget = vtkSplineWidget()
spline_widget.SetCurrentRenderer(renderer_1)
spline_widget.SetDefaultRenderer(renderer_1)
spline_widget.SetInputConnection(extract.GetOutputPort())
spline_widget.SetInteractor(interactor)
spline_widget.PlaceWidget(image_actor_1.GetBounds())
spline_widget.ProjectToPlaneOn()
spline_widget.SetProjectionNormalToXAxes()
spline_widget.SetProjectionPosition(image_actor_1.GetBounds()[0])
spline_widget.AddObserver(vtkCommand.EndInteractionEvent, spline_callback)
spline_widget.On()

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

cam_0 = renderer_0.GetActiveCamera()
cam_0.SetViewUp(0, 1, 0)
cam_0.Azimuth(270)
cam_0.Roll(270)
cam_0.Dolly(1.7)
renderer_0.ResetCameraClippingRange()

cam_1 = renderer_1.GetActiveCamera()
cam_1.SetViewUp(0, 1, 0)
cam_1.Azimuth(270)
cam_1.Roll(270)
cam_1.Dolly(1.7)
renderer_1.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
