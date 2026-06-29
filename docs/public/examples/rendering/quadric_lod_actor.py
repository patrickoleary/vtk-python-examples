#!/usr/bin/env python

# Demonstrate vtkQuadricLODActor with a sphere and plane source.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkQuadricLODActor

colors = vtkNamedColors()
tomato_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("tomato", tomato_rgb)

# Sphere and plane sources
sphere = vtkSphereSource()
sphere.SetPhiResolution(150)
sphere.SetThetaResolution(150)

plane = vtkPlaneSource()
plane.SetXResolution(150)
plane.SetYResolution(150)

# Mapper + Actor
lod_mapper = vtkPolyDataMapper()
lod_mapper.SetInputConnection(sphere.GetOutputPort())
lod_mapper.SetInputConnection(plane.GetOutputPort())

lod_actor = vtkQuadricLODActor()
lod_actor.SetMapper(lod_mapper)
lod_actor.DeferLODConstructionOff()
lod_actor.GetProperty().SetRepresentationToWireframe()
lod_actor.GetProperty().SetDiffuseColor(tomato_rgb)
lod_actor.GetProperty().SetDiffuse(0.8)
lod_actor.GetProperty().SetSpecular(0.4)
lod_actor.GetProperty().SetSpecularPower(30)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(lod_actor)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("quadric lod actor")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
