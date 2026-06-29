#!/usr/bin/env python

# Demonstrate vtkClipClosedSurface with inside-out flag and second output
# by clipping an isosurface extracted from a volume dataset, showing
# the clipped surface, the inside-out surface, and the clip face.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPlaneCollection,
)
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkFiltersGeneral import vtkClipClosedSurface
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
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

# Read volume data
reader = vtkVolume16Reader()
reader.SetDataDimensions(64, 64)
reader.SetDataOrigin(0, 0, 0)
reader.SetDataByteOrderToLittleEndian()
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetImageRange(1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.Update()

# Smooth the volume
smooth = vtkImageGaussianSmooth()
smooth.SetDimensionality(3)
smooth.SetInputConnection(reader.GetOutputPort())
smooth.SetStandardDeviations(1.75, 1.75, 0)
smooth.SetRadiusFactor(3)

# Extract isosurface
iso = vtkFlyingEdges3D()
iso.SetInputConnection(smooth.GetOutputPort())
iso.SetValue(0, 1150)

# Define clip plane
plane_normal = [0.88, 0.47, -0.1]
clip_plane = vtkPlane()
clip_plane.SetNormal(plane_normal)
clip_plane.SetOrigin(105, 125, 60)

cap_planes = vtkPlaneCollection()
cap_planes.AddItem(clip_plane)

# Clip closed surface
clip = vtkClipClosedSurface()
clip.SetClippingPlanes(cap_planes)
clip.SetInputConnection(iso.GetOutputPort())
clip.SetBaseColor(0.9804, 0.9216, 0.8431)
clip.SetClipColor(1.0, 1.0, 1.0)
clip.SetScalarModeToColors()
clip.GenerateFacesOn()
clip.GenerateClipFaceOutputOn()
clip.GenerateOutlineOn()

clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clip.GetOutputPort())

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)

# Inside-out clip surface
clip_inside = vtkClipClosedSurface()
clip_inside.SetClippingPlanes(cap_planes)
clip_inside.SetInputConnection(iso.GetOutputPort())
clip_inside.SetBaseColor(0.9804, 0.9216, 0.8431)
clip_inside.SetClipColor(1.0, 1.0, 1.0)
clip_inside.SetScalarModeToColors()
clip_inside.GenerateFacesOn()
clip_inside.InsideOutOn()

# Translate the inverse clipped volume to create a gap
translate = vtkTransform()
translate.Translate(
    -plane_normal[0] * 50, -plane_normal[1] * 50, -plane_normal[2] * 50
)

clip_inside_mapper = vtkPolyDataMapper()
clip_inside_mapper.SetInputConnection(clip_inside.GetOutputPort())

clip_inside_actor = vtkActor()
clip_inside_actor.SetUserTransform(translate)
clip_inside_actor.SetMapper(clip_inside_mapper)

# Clip face output (second output port)
translate_face = vtkTransform()
translate_face.Translate(
    -plane_normal[0] * 25, -plane_normal[1] * 25, -plane_normal[2] * 25
)

clip_face_mapper = vtkPolyDataMapper()
clip_face_mapper.SetInputConnection(clip.GetOutputPort(1))

clip_face_actor = vtkActor()
clip_face_actor.SetUserTransform(translate_face)
clip_face_actor.SetMapper(clip_face_mapper)
clip_face_actor.GetProperty().SetColor(0.18, 0.54, 0.34)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(clip_inside_actor)
renderer.AddActor(clip_face_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(301, 300)
render_window.SetWindowName("clip closed surface inside out")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(-244.6, 367.4, 102.54)
renderer.GetActiveCamera().SetFocalPoint(78.55, 85.95, 71.5)
renderer.GetActiveCamera().SetViewUp(0, 0, -1)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
