#!/usr/bin/env python
# Demonstrate more parametric surfaces: Kuen, Pseudosphere, Bohemian Dome, Henneberg, Catalan, Bour, Plucker.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonComputationalGeometry import (
    vtkParametricBohemianDome,
    vtkParametricBour,
    vtkParametricCatalanMinimal,
    vtkParametricHenneberg,
    vtkParametricKuen,
    vtkParametricPluckerConoid,
    vtkParametricPseudosphere,
)
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
)

# Kuen's surface.
kuen = vtkParametricKuen()
kuen_source = vtkParametricFunctionSource()
kuen_source.SetParametricFunction(kuen)
kuen_source.SetScalarModeToU()

kuen_mapper = vtkPolyDataMapper()
kuen_mapper.SetInputConnection(kuen_source.GetOutputPort())

kuen_actor = vtkActor()
kuen_actor.SetMapper(kuen_mapper)
kuen_actor.SetPosition(0, -19, 0)
kuen_actor.RotateX(90)

kuen_text_mapper = vtkTextMapper()
kuen_text_mapper.SetInput("Kuen")
kuen_text_mapper.GetTextProperty().SetJustificationToCentered()
kuen_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
kuen_text_mapper.GetTextProperty().SetColor(1, 0, 0)
kuen_text_mapper.GetTextProperty().SetFontSize(14)
kuen_text_actor = vtkActor2D()
kuen_text_actor.SetMapper(kuen_text_mapper)
kuen_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
kuen_text_actor.GetPositionCoordinate().SetValue(0, -22.5, 0)

# Pseudosphere.
pseudo = vtkParametricPseudosphere()
pseudo.SetMinimumU(-3)
pseudo.SetMaximumU(3)
pseudo_source = vtkParametricFunctionSource()
pseudo_source.SetParametricFunction(pseudo)
pseudo_source.SetScalarModeToY()

pseudo_mapper = vtkPolyDataMapper()
pseudo_mapper.SetInputConnection(pseudo_source.GetOutputPort())

pseudo_actor = vtkActor()
pseudo_actor.SetMapper(pseudo_mapper)
pseudo_actor.SetPosition(8, -19, 0)
pseudo_actor.RotateX(90)

pseudo_text_mapper = vtkTextMapper()
pseudo_text_mapper.SetInput("Pseudosphere")
pseudo_text_mapper.GetTextProperty().SetJustificationToCentered()
pseudo_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
pseudo_text_mapper.GetTextProperty().SetColor(1, 0, 0)
pseudo_text_mapper.GetTextProperty().SetFontSize(14)
pseudo_text_actor = vtkActor2D()
pseudo_text_actor.SetMapper(pseudo_text_mapper)
pseudo_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
pseudo_text_actor.GetPositionCoordinate().SetValue(8, -22.5, 0)

# Bohemian Dome.
bdome = vtkParametricBohemianDome()
bdome_source = vtkParametricFunctionSource()
bdome_source.SetParametricFunction(bdome)
bdome_source.SetScalarModeToU()

bdome_mapper = vtkPolyDataMapper()
bdome_mapper.SetInputConnection(bdome_source.GetOutputPort())

bdome_actor = vtkActor()
bdome_actor.SetMapper(bdome_mapper)
bdome_actor.SetPosition(16, -19, 0)
bdome_actor.RotateY(90)

bdome_text_mapper = vtkTextMapper()
bdome_text_mapper.SetInput("Bohemian Dome")
bdome_text_mapper.GetTextProperty().SetJustificationToCentered()
bdome_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
bdome_text_mapper.GetTextProperty().SetColor(1, 0, 0)
bdome_text_mapper.GetTextProperty().SetFontSize(14)
bdome_text_actor = vtkActor2D()
bdome_text_actor.SetMapper(bdome_text_mapper)
bdome_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
bdome_text_actor.GetPositionCoordinate().SetValue(16, -22.5, 0)

# Henneberg's minimal surface.
hberg = vtkParametricHenneberg()
hberg.SetMinimumU(-0.3)
hberg.SetMaximumU(0.3)
hberg_source = vtkParametricFunctionSource()
hberg_source.SetParametricFunction(hberg)
hberg_source.SetScalarModeToV()

hberg_mapper = vtkPolyDataMapper()
hberg_mapper.SetInputConnection(hberg_source.GetOutputPort())

hberg_actor = vtkActor()
hberg_actor.SetMapper(hberg_mapper)
hberg_actor.SetPosition(24, -19, 0)
hberg_actor.RotateY(90)

hberg_text_mapper = vtkTextMapper()
hberg_text_mapper.SetInput("Henneberg")
hberg_text_mapper.GetTextProperty().SetJustificationToCentered()
hberg_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
hberg_text_mapper.GetTextProperty().SetColor(1, 0, 0)
hberg_text_mapper.GetTextProperty().SetFontSize(14)
hberg_text_actor = vtkActor2D()
hberg_text_actor.SetMapper(hberg_text_mapper)
hberg_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
hberg_text_actor.GetPositionCoordinate().SetValue(24, -22.5, 0)

# Catalan's minimal surface.
catalan = vtkParametricCatalanMinimal()
catalan.SetMinimumU(-2.0 * math.pi)
catalan.SetMaximumU(2.0 * math.pi)
catalan_source = vtkParametricFunctionSource()
catalan_source.SetParametricFunction(catalan)
catalan_source.SetScalarModeToV()

catalan_mapper = vtkPolyDataMapper()
catalan_mapper.SetInputConnection(catalan_source.GetOutputPort())

catalan_actor = vtkActor()
catalan_actor.SetMapper(catalan_mapper)
catalan_actor.SetPosition(0, -27, 0)
catalan_actor.SetScale(0.5, 0.5, 0.5)

catalan_text_mapper = vtkTextMapper()
catalan_text_mapper.SetInput("Catalan")
catalan_text_mapper.GetTextProperty().SetJustificationToCentered()
catalan_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
catalan_text_mapper.GetTextProperty().SetColor(1, 0, 0)
catalan_text_mapper.GetTextProperty().SetFontSize(14)
catalan_text_actor = vtkActor2D()
catalan_text_actor.SetMapper(catalan_text_mapper)
catalan_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
catalan_text_actor.GetPositionCoordinate().SetValue(0, -30.5, 0)

# Bour's minimal surface.
bour = vtkParametricBour()
bour_source = vtkParametricFunctionSource()
bour_source.SetParametricFunction(bour)
bour_source.SetScalarModeToU()

bour_mapper = vtkPolyDataMapper()
bour_mapper.SetInputConnection(bour_source.GetOutputPort())

bour_actor = vtkActor()
bour_actor.SetMapper(bour_mapper)
bour_actor.SetPosition(8, -27, 0)

bour_text_mapper = vtkTextMapper()
bour_text_mapper.SetInput("Bour")
bour_text_mapper.GetTextProperty().SetJustificationToCentered()
bour_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
bour_text_mapper.GetTextProperty().SetColor(1, 0, 0)
bour_text_mapper.GetTextProperty().SetFontSize(14)
bour_text_actor = vtkActor2D()
bour_text_actor.SetMapper(bour_text_mapper)
bour_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
bour_text_actor.GetPositionCoordinate().SetValue(8, -30.5, 0)

# Plucker's conoid surface.
plucker = vtkParametricPluckerConoid()
plucker_source = vtkParametricFunctionSource()
plucker_source.SetParametricFunction(plucker)
plucker_source.SetScalarModeToZ()

plucker_mapper = vtkPolyDataMapper()
plucker_mapper.SetInputConnection(plucker_source.GetOutputPort())

plucker_actor = vtkActor()
plucker_actor.SetMapper(plucker_mapper)
plucker_actor.SetPosition(16, -27, 0)

plucker_text_mapper = vtkTextMapper()
plucker_text_mapper.SetInput("Plucker")
plucker_text_mapper.GetTextProperty().SetJustificationToCentered()
plucker_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
plucker_text_mapper.GetTextProperty().SetColor(1, 0, 0)
plucker_text_mapper.GetTextProperty().SetFontSize(14)
plucker_text_actor = vtkActor2D()
plucker_text_actor.SetMapper(plucker_text_mapper)
plucker_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
plucker_text_actor.GetPositionCoordinate().SetValue(16, -30.5, 0)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(kuen_actor)
renderer.AddActor(pseudo_actor)
renderer.AddActor(bdome_actor)
renderer.AddActor(hberg_actor)
renderer.AddActor(catalan_actor)
renderer.AddActor(bour_actor)
renderer.AddActor(plucker_actor)
renderer.AddActor(kuen_text_actor)
renderer.AddActor(pseudo_text_actor)
renderer.AddActor(bdome_text_actor)
renderer.AddActor(hberg_text_actor)
renderer.AddActor(catalan_text_actor)
renderer.AddActor(bour_text_actor)
renderer.AddActor(plucker_text_actor)

renderer.SetBackground(0.9, 0.9, 0.9)

render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)
render_window.SetWindowName("more parametric functions")

renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
