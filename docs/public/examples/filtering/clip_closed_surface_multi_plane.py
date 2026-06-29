#!/usr/bin/env python

# Demonstrate vtkClipClosedSurface with multiple clipping planes on a
# superquadric, showing the clipped surface and the triangulated clip face.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPlaneCollection,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkClipClosedSurface
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create superquadric source
source = vtkSuperquadricSource()
source.SetPhiResolution(24)
source.SetPhiRoundness(0.5)
source.SetThetaResolution(24)
source.SetThetaRoundness(0.5)

# Define clipping planes
clip_plane_1 = vtkPlane()
clip_plane_1.SetOrigin(0.27, -0.16, 0.46)
clip_plane_1.SetNormal(0.48, -0.29, 0.83)

clip_plane_2 = vtkPlane()
clip_plane_2.SetOrigin(-0.39, 0.22, 0.30)
clip_plane_2.SetNormal(-0.8, -0.31, 0.5)

clip_plane_3 = vtkPlane()
clip_plane_3.SetOrigin(0.16, -0.19, 0.42)
clip_plane_3.SetNormal(0.0, -0.95, 0.31)

# Group planes
planes = vtkPlaneCollection()
planes.AddItem(clip_plane_1)
planes.AddItem(clip_plane_2)
planes.AddItem(clip_plane_3)

# Clip closed surface
clip = vtkClipClosedSurface()
clip.SetClippingPlanes(planes)
clip.SetInputConnection(source.GetOutputPort())
clip.SetBaseColor(0.44, 0.31, 0.31)
clip.SetClipColor(0.87, 0.63, 0.87)
clip.SetScalarModeToColors()
clip.GenerateClipFaceOutputOn()
clip.GenerateFacesOn()
clip.GenerateOutlineOff()
clip.InsideOutOn()

# Clip actor
clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clip.GetOutputPort())

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetDiffuse(0.5)
clip_actor.GetProperty().SetAmbient(0.5)

# Clip face (second output port), translated along plane 3 normal
n = list(clip_plane_3.GetNormal())
translate = vtkTransform()
translate.Translate(n[0] * 0.5, n[1] * 0.5, n[2] * 0.5)

clip_face_mapper = vtkPolyDataMapper()
clip_face_mapper.SetInputConnection(clip.GetOutputPort(1))

clip_face_actor = vtkActor()
clip_face_actor.SetMapper(clip_face_mapper)
clip_face_actor.SetUserTransform(translate)
clip_face_actor.GetProperty().SetColor(0.18, 0.54, 0.34)
clip_face_actor.GetProperty().SetDiffuse(0.5)
clip_face_actor.GetProperty().SetAmbient(0.5)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(clip_face_actor)
renderer.SetBackground(0.3, 0.3, 0.32)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(301, 300)
render_window.SetWindowName("clip closed surface multi plane")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetViewUp(0, -1, 0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
