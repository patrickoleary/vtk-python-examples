#!/usr/bin/env python

# Test scalar coloring interactions with ambient/diffuse property settings.
# Modern replacement for the removed SetScalarMaterialMode API.
# Material control now lives on vtkProperty (ambient, diffuse, specular)
# while scalar mapping is handled by the mapper's lookup table and scalar mode.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Shared pipeline
sphere = vtkSphereSource()

elev = vtkElevationFilter()
elev.SetLowPoint(-0.25, -0.25, -0.25)
elev.SetHighPoint(0.25, 0.25, 0.25)
elev.SetInputConnection(sphere.GetOutputPort())

lut = vtkLookupTable()
lut.SetSaturationRange(0, 0)
lut.SetValueRange(0, 1)
lut.SetRange(0, 1)
lut.Build()

# Viewport 0: Diffuse only, interpolate=1
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(elev.GetOutputPort())
mapper_0.SetLookupTable(lut)
mapper_0.SetScalarModeToUsePointData()
mapper_0.SetInterpolateScalarsBeforeMapping(1)
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
prop_0 = actor_0.GetProperty()
prop_0.SetAmbient(0.0)
prop_0.SetDiffuse(1.0)
prop_0.SetAmbientColor(1, 0, 0)
prop_0.SetDiffuseColor(0, 1, 0)
text_actor_0 = vtkTextActor()
text_actor_0.SetInput(
    " InterpolateScalarsBeforeMapping: 1\n"
    " Mode: Diffuse only\n"
    " Ambient: 0.00\t Ambient Color: 1, 0, 0\n"
    " Diffuse: 1.00\t Diffuse Color: 0, 1, 0")
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.5, 0.5, 0.5)
renderer_0.SetViewport(0, 0, 0.5, 0.25)
renderer_0.AddActor(actor_0)
renderer_0.AddActor(text_actor_0)

# Viewport 1: Diffuse only, interpolate=0
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(elev.GetOutputPort())
mapper_1.SetLookupTable(lut)
mapper_1.SetScalarModeToUsePointData()
mapper_1.SetInterpolateScalarsBeforeMapping(0)
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
prop_1 = actor_1.GetProperty()
prop_1.SetAmbient(0.0)
prop_1.SetDiffuse(1.0)
prop_1.SetAmbientColor(1, 0, 0)
prop_1.SetDiffuseColor(0, 1, 0)
text_actor_1 = vtkTextActor()
text_actor_1.SetInput(
    " InterpolateScalarsBeforeMapping: 0\n"
    " Mode: Diffuse only\n"
    " Ambient: 0.00\t Ambient Color: 1, 0, 0\n"
    " Diffuse: 1.00\t Diffuse Color: 0, 1, 0")
renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.5, 0.5, 0.5)
renderer_1.SetViewport(0.5, 0, 1, 0.25)
renderer_1.AddActor(actor_1)
renderer_1.AddActor(text_actor_1)

# Viewport 2: Ambient only, interpolate=1
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(elev.GetOutputPort())
mapper_2.SetLookupTable(lut)
mapper_2.SetScalarModeToUsePointData()
mapper_2.SetInterpolateScalarsBeforeMapping(1)
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
prop_2 = actor_2.GetProperty()
prop_2.SetAmbient(1.0)
prop_2.SetDiffuse(0.0)
prop_2.SetAmbientColor(1, 0, 0)
prop_2.SetDiffuseColor(0, 1, 0)
text_actor_2 = vtkTextActor()
text_actor_2.SetInput(
    " InterpolateScalarsBeforeMapping: 1\n"
    " Mode: Ambient only\n"
    " Ambient: 1.00\t Ambient Color: 1, 0, 0\n"
    " Diffuse: 0.00\t Diffuse Color: 0, 1, 0")
renderer_2 = vtkRenderer()
renderer_2.SetBackground(0.5, 0.5, 0.5)
renderer_2.SetViewport(0, 0.25, 0.5, 0.5)
renderer_2.AddActor(actor_2)
renderer_2.AddActor(text_actor_2)

# Viewport 3: Ambient only, interpolate=0
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(elev.GetOutputPort())
mapper_3.SetLookupTable(lut)
mapper_3.SetScalarModeToUsePointData()
mapper_3.SetInterpolateScalarsBeforeMapping(0)
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
prop_3 = actor_3.GetProperty()
prop_3.SetAmbient(1.0)
prop_3.SetDiffuse(0.0)
prop_3.SetAmbientColor(1, 0, 0)
prop_3.SetDiffuseColor(0, 1, 0)
text_actor_3 = vtkTextActor()
text_actor_3.SetInput(
    " InterpolateScalarsBeforeMapping: 0\n"
    " Mode: Ambient only\n"
    " Ambient: 1.00\t Ambient Color: 1, 0, 0\n"
    " Diffuse: 0.00\t Diffuse Color: 0, 1, 0")
renderer_3 = vtkRenderer()
renderer_3.SetBackground(0.5, 0.5, 0.5)
renderer_3.SetViewport(0.5, 0.25, 1, 0.5)
renderer_3.AddActor(actor_3)
renderer_3.AddActor(text_actor_3)

# Viewport 4: Ambient + Diffuse, interpolate=1
mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(elev.GetOutputPort())
mapper_4.SetLookupTable(lut)
mapper_4.SetScalarModeToUsePointData()
mapper_4.SetInterpolateScalarsBeforeMapping(1)
actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
prop_4 = actor_4.GetProperty()
prop_4.SetAmbient(0.49)
prop_4.SetDiffuse(0.51)
prop_4.SetAmbientColor(1, 0, 0)
prop_4.SetDiffuseColor(0, 1, 0)
text_actor_4 = vtkTextActor()
text_actor_4.SetInput(
    " InterpolateScalarsBeforeMapping: 1\n"
    " Mode: Ambient + Diffuse\n"
    " Ambient: 0.49\t Ambient Color: 1, 0, 0\n"
    " Diffuse: 0.51\t Diffuse Color: 0, 1, 0")
renderer_4 = vtkRenderer()
renderer_4.SetBackground(0.5, 0.5, 0.5)
renderer_4.SetViewport(0, 0.5, 0.5, 0.75)
renderer_4.AddActor(actor_4)
renderer_4.AddActor(text_actor_4)

# Viewport 5: Ambient + Diffuse, interpolate=0
mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(elev.GetOutputPort())
mapper_5.SetLookupTable(lut)
mapper_5.SetScalarModeToUsePointData()
mapper_5.SetInterpolateScalarsBeforeMapping(0)
actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
prop_5 = actor_5.GetProperty()
prop_5.SetAmbient(0.49)
prop_5.SetDiffuse(0.51)
prop_5.SetAmbientColor(1, 0, 0)
prop_5.SetDiffuseColor(0, 1, 0)
text_actor_5 = vtkTextActor()
text_actor_5.SetInput(
    " InterpolateScalarsBeforeMapping: 0\n"
    " Mode: Ambient + Diffuse\n"
    " Ambient: 0.49\t Ambient Color: 1, 0, 0\n"
    " Diffuse: 0.51\t Diffuse Color: 0, 1, 0")
renderer_5 = vtkRenderer()
renderer_5.SetBackground(0.5, 0.5, 0.5)
renderer_5.SetViewport(0.5, 0.5, 1, 0.75)
renderer_5.AddActor(actor_5)
renderer_5.AddActor(text_actor_5)

# Viewport 6: No lighting, interpolate=1
mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(elev.GetOutputPort())
mapper_6.SetLookupTable(lut)
mapper_6.SetScalarModeToUsePointData()
mapper_6.SetInterpolateScalarsBeforeMapping(1)
actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
prop_6 = actor_6.GetProperty()
prop_6.SetAmbient(0.0)
prop_6.SetDiffuse(0.0)
prop_6.SetAmbientColor(1, 0, 0)
prop_6.SetDiffuseColor(0, 1, 0)
text_actor_6 = vtkTextActor()
text_actor_6.SetInput(
    " InterpolateScalarsBeforeMapping: 1\n"
    " Mode: No lighting\n"
    " Ambient: 0.00\t Ambient Color: 1, 0, 0\n"
    " Diffuse: 0.00\t Diffuse Color: 0, 1, 0")
renderer_6 = vtkRenderer()
renderer_6.SetBackground(0.5, 0.5, 0.5)
renderer_6.SetViewport(0, 0.75, 0.5, 1)
renderer_6.AddActor(actor_6)
renderer_6.AddActor(text_actor_6)

# Viewport 7: No lighting, interpolate=0
mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(elev.GetOutputPort())
mapper_7.SetLookupTable(lut)
mapper_7.SetScalarModeToUsePointData()
mapper_7.SetInterpolateScalarsBeforeMapping(0)
actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
prop_7 = actor_7.GetProperty()
prop_7.SetAmbient(0.0)
prop_7.SetDiffuse(0.0)
prop_7.SetAmbientColor(1, 0, 0)
prop_7.SetDiffuseColor(0, 1, 0)
text_actor_7 = vtkTextActor()
text_actor_7.SetInput(
    " InterpolateScalarsBeforeMapping: 0\n"
    " Mode: No lighting\n"
    " Ambient: 0.00\t Ambient Color: 1, 0, 0\n"
    " Diffuse: 0.00\t Diffuse Color: 0, 1, 0")
renderer_7 = vtkRenderer()
renderer_7.SetBackground(0.5, 0.5, 0.5)
renderer_7.SetViewport(0.5, 0.75, 1, 1)
renderer_7.AddActor(actor_7)
renderer_7.AddActor(text_actor_7)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.SetWindowName("scalar material mode")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 600)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
