#!/usr/bin/env python
# Demonstrate vtkHandleWidget with vtkConstrainedPointHandleRepresentation on an image slice.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkInteractionWidgets import (
    vtkConstrainedPointHandleRepresentation,
    vtkHandleWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

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

# Actor: coronal slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shifter.GetOutputPort())
image_actor.VisibilityOn()
image_actor.SetDisplayExtent(0, 63, 30, 30, 0, 92)
image_actor.InterpolateOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("constrained handle widget")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
handle_rep = vtkConstrainedPointHandleRepresentation()
handle_rep.ActiveRepresentationOn()
handle_rep.SetPosition(image_actor.GetCenter())
handle_rep.SetProjectionNormalToYAxis()
handle_rep.SetProjectionPosition(image_actor.GetCenter()[1])

# Add bounding planes to constrain the handle
bounds = image_actor.GetBounds()

bounding_plane_1 = vtkPlane()
bounding_plane_1.SetOrigin(bounds[0], bounds[2], bounds[4])
bounding_plane_1.SetNormal(1.0, 0.0, 0.0)

bounding_plane_2 = vtkPlane()
bounding_plane_2.SetOrigin(bounds[0], bounds[2], bounds[4])
bounding_plane_2.SetNormal(0.0, 0.0, 1.0)

bounding_plane_3 = vtkPlane()
bounding_plane_3.SetOrigin(bounds[1], bounds[3], bounds[5])
bounding_plane_3.SetNormal(-1.0, 0.0, 0.0)

bounding_plane_4 = vtkPlane()
bounding_plane_4.SetOrigin(bounds[1], bounds[3], bounds[5])
bounding_plane_4.SetNormal(0.0, 0.0, -1.0)

handle_rep.AddBoundingPlane(bounding_plane_1)
handle_rep.AddBoundingPlane(bounding_plane_2)
handle_rep.AddBoundingPlane(bounding_plane_3)
handle_rep.AddBoundingPlane(bounding_plane_4)

handle_widget = vtkHandleWidget()
handle_widget.SetInteractor(interactor)
handle_widget.SetRepresentation(handle_rep)

# Scene
renderer.GetActiveCamera().SetPosition(0, 0, 0)
renderer.GetActiveCamera().SetFocalPoint(0, 1, 0)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
