#!/usr/bin/env python
# Demonstrate vtkContourWidget with oriented glyph representation on a medical image slice.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkInteractionWidgets import (
    vtkBoundedPlanePointPlacer,
    vtkContourWidget,
    vtkOrientedGlyphContourRepresentation,
    vtkWidgetEvent,
)
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: volume data
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
file_prefix = os.path.join(data_dir, "headsq", "quarter")

volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.SetDataByteOrderToLittleEndian()
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)
volume_reader.SetFilePrefix(file_prefix)
volume_reader.ReleaseDataFlagOn()
volume_reader.SetDataMask(0x7FFF)
volume_reader.Update()

# Filter
scalar_range = volume_reader.GetOutput().GetScalarRange()
shifter = vtkImageShiftScale()
shifter.SetShift(-1.0 * scalar_range[0])
shifter.SetScale(255.0 / (scalar_range[1] - scalar_range[0]))
shifter.SetOutputScalarTypeToUnsignedChar()
shifter.SetInputConnection(volume_reader.GetOutputPort())
shifter.ReleaseDataFlagOff()
shifter.Update()

# Actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shifter.GetOutputPort())
image_actor.VisibilityOn()
image_actor.SetDisplayExtent(0, 63, 0, 63, 46, 46)
image_actor.InterpolateOn()

# Bounding planes from image actor bounds
bounds = image_actor.GetBounds()

bounding_plane_1 = vtkPlane()
bounding_plane_1.SetOrigin(bounds[0], bounds[2], bounds[4])
bounding_plane_1.SetNormal(1.0, 0.0, 0.0)

bounding_plane_2 = vtkPlane()
bounding_plane_2.SetOrigin(bounds[0], bounds[2], bounds[4])
bounding_plane_2.SetNormal(0.0, 1.0, 0.0)

bounding_plane_3 = vtkPlane()
bounding_plane_3.SetOrigin(bounds[1], bounds[3], bounds[5])
bounding_plane_3.SetNormal(-1.0, 0.0, 0.0)

bounding_plane_4 = vtkPlane()
bounding_plane_4.SetOrigin(bounds[1], bounds[3], bounds[5])
bounding_plane_4.SetNormal(0.0, -1.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("oriented glyph contour")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
contour_rep = vtkOrientedGlyphContourRepresentation()

placer = vtkBoundedPlanePointPlacer()
placer.SetProjectionNormalToZAxis()
placer.SetProjectionPosition(image_actor.GetCenter()[2])
placer.AddBoundingPlane(bounding_plane_1)
placer.AddBoundingPlane(bounding_plane_2)
placer.AddBoundingPlane(bounding_plane_3)
placer.AddBoundingPlane(bounding_plane_4)

contour_rep.SetPointPlacer(placer)

contour_widget = vtkContourWidget()
contour_widget.SetInteractor(interactor)
contour_widget.SetRepresentation(contour_rep)

event_translator = contour_widget.GetEventTranslator()
event_translator.RemoveTranslation("RightButtonPressEvent")
event_translator.SetTranslation(
    vtkCommand.KeyPressEvent, 0, "g", 0, "g", vtkWidgetEvent.AddFinalPoint
)
event_translator.SetTranslation(vtkCommand.RightButtonPressEvent, vtkWidgetEvent.Translate)
contour_widget.On()

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(0, 0, 0)
camera.SetFocalPoint(0, 0, 1)
camera.SetViewUp(0, 1, 0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
