#!/usr/bin/env python

# Clip a sphere with two planes using vtkClipClosedSurface, showing
# the clipped surface, outline, and the clipped bounding box outline.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPlaneCollection,
)
from vtkmodules.vtkFiltersCore import vtkStripper
from vtkmodules.vtkFiltersGeneral import vtkClipClosedSurface
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere and clip it
sphere = vtkSphereSource()
sphere.SetRadius(1)
sphere.SetPhiResolution(10)
sphere.SetThetaResolution(10)

plane_1 = vtkPlane()
plane_1.SetOrigin(0.3, 0.3, 0.3)
plane_1.SetNormal(-1, -1, -1)

plane_2 = vtkPlane()
plane_2.SetOrigin(0.5, 0, 0)
plane_2.SetNormal(-1, 0, 0)

planes = vtkPlaneCollection()
planes.AddItem(plane_1)
planes.AddItem(plane_2)

# Stripper increases coverage
stripper = vtkStripper()
stripper.SetInputConnection(sphere.GetOutputPort())

# Clip with filled faces
clipper = vtkClipClosedSurface()
clipper.SetInputConnection(stripper.GetOutputPort())
clipper.SetClippingPlanes(planes)

# Clip with outline only
clipper_outline = vtkClipClosedSurface()
clipper_outline.SetInputConnection(stripper.GetOutputPort())
clipper_outline.SetClippingPlanes(planes)
clipper_outline.GenerateFacesOff()
clipper_outline.GenerateOutlineOn()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(clipper.GetOutputPort())

clipper_outline_mapper = vtkPolyDataMapper()
clipper_outline_mapper.SetInputConnection(clipper_outline.GetOutputPort())

clip_actor = vtkActor()
clip_actor.SetMapper(sphere_mapper)
clip_actor.GetProperty().SetColor(0.8, 0.05, 0.2)

clip_outline_actor = vtkActor()
clip_outline_actor.SetMapper(clipper_outline_mapper)
clip_outline_actor.GetProperty().SetColor(0, 1, 0)
clip_outline_actor.SetPosition(0.001, 0.001, 0.001)

# Create an outline of the bounding box and clip it
outline = vtkOutlineFilter()
outline.SetInputConnection(sphere.GetOutputPort())
outline.GenerateFacesOn()

outline_clip = vtkClipClosedSurface()
outline_clip.SetClippingPlanes(planes)
outline_clip.SetInputConnection(outline.GetOutputPort())
outline_clip.GenerateFacesOff()
outline_clip.GenerateOutlineOn()
outline_clip.SetScalarModeToColors()
outline_clip.SetClipColor(0, 1, 0)

outline_mapper = vtkDataSetMapper()
outline_mapper.SetInputConnection(outline_clip.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.SetPosition(0.001, 0.001, 0.001)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(clip_outline_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("clip outline")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
