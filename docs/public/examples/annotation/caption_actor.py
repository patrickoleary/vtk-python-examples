#!/usr/bin/env python

# Demonstrate vtkCaptionActor2D with leader glyphs on a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkCaptionActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
sphere_source = vtkSphereSource()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Glyph sources for leader
cone_glyph = vtkConeSource()
cone_glyph.SetResolution(6)

# Caption 1 — south pole with 3D leader and cone glyph
south_pole_caption = vtkCaptionActor2D()
south_pole_caption.SetCaption("This is the\nsouth pole")
south_pole_caption.SetAttachmentPoint(0, 0, -0.5)
south_pole_caption.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
south_pole_caption.GetPositionCoordinate().SetReferenceCoordinate(None)
south_pole_caption.GetPositionCoordinate().SetValue(0.05, 0.05)
south_pole_caption.SetWidth(0.25)
south_pole_caption.SetHeight(0.15)
south_pole_caption.ThreeDimensionalLeaderOn()
south_pole_caption.SetLeaderGlyphConnection(cone_glyph.GetOutputPort())
south_pole_caption.SetMaximumLeaderGlyphSize(10)
south_pole_caption.SetLeaderGlyphSize(0.025)
south_pole_caption.GetProperty().SetColor(1, 0, 0)
south_pole_caption.GetCaptionTextProperty().SetColor(south_pole_caption.GetProperty().GetColor())

# Caption 2 — north pole without border
north_pole_caption = vtkCaptionActor2D()
north_pole_caption.SetCaption("Santa lives here")
north_pole_caption.GetProperty().SetColor(1, 0, 0)
north_pole_caption.SetAttachmentPoint(0, 0, 0.5)
north_pole_caption.SetHeight(0.05)
north_pole_caption.BorderOff()
north_pole_caption.SetPosition(25, 10)
north_pole_caption.ThreeDimensionalLeaderOff()
north_pole_caption.SetLeaderGlyphConnection(cone_glyph.GetOutputPort())
north_pole_caption.SetWidth(0.35)
north_pole_caption.SetHeight(0.10)
north_pole_caption.SetMaximumLeaderGlyphSize(10)
north_pole_caption.SetLeaderGlyphSize(0.025)
north_pole_caption.GetCaptionTextProperty().SetColor(north_pole_caption.GetProperty().GetColor())

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(north_pole_caption)
renderer.AddViewProp(south_pole_caption)
renderer.AddActor(sphere_actor)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("caption actor")
render_window.SetMultiSamples(0)
render_window.SetSize(250, 250)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetPosition(1, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
