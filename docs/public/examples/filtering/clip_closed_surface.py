#!/usr/bin/env python

# Clip a marching cubes isosurface of CT head data with multiple planes
# using vtkClipClosedSurface, generating capped faces and outlines.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPlaneCollection,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkClipClosedSurface,
    vtkImageMarchingCubes,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read CT head data
v16 = vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.GetOutput().SetOrigin(0.0, 0.0, 0.0)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.Update()

# Extract isosurface
iso = vtkImageMarchingCubes()
iso.SetInputConnection(v16.GetOutputPort())
iso.SetValue(0, 1150)
iso.SetInputMemoryLimit(1000)

# Define clipping planes
top_plane = vtkPlane()
top_plane.SetNormal(0, 0, 1)
top_plane.SetOrigin(0, 0, 0.5)

bot_plane = vtkPlane()
bot_plane.SetNormal(0, 0, -1)
bot_plane.SetOrigin(0, 0, 137.0)

sag_plane = vtkPlane()
sag_plane.SetNormal(1, 0, 0)
sag_plane.SetOrigin(100.8, 0, 0)

cap_planes = vtkPlaneCollection()
cap_planes.AddItem(top_plane)
cap_planes.AddItem(bot_plane)
cap_planes.AddItem(sag_plane)

# Clip the isosurface
clip = vtkClipClosedSurface()
clip.SetClippingPlanes(cap_planes)
clip.SetInputConnection(iso.GetOutputPort())
clip.SetBaseColor(0.9804, 0.9216, 0.8431)
clip.SetClipColor(1.0, 1.0, 1.0)
clip.SetActivePlaneColor(1.0, 1.0, 0.8)
clip.SetActivePlaneId(2)
clip.SetScalarModeToColors()
clip.GenerateOutlineOn()
clip.GenerateFacesOn()

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(clip.GetOutputPort())
iso_mapper.ScalarVisibilityOn()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(v16.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.VisibilityOff()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("clip closed surface")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(90)
renderer.GetActiveCamera().SetViewUp(0, 0, -1)
renderer.GetActiveCamera().Azimuth(270)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
